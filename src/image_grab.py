import boto
import cStringIO
import urllib
import Image
from pymongo import MongoClient



if __name__ == '__main__':
    client = MongoClient()
    db = client.products
    rei = db.rei


    for entries in rei.find({}):
        title = entries['title']
        links = entries['img_links'])
        for url in links:
            #Retrieve our source image from a URL
        fp = urllib.urlopen(url)

        #Load the URL data into an image
        img = cStringIO.StringIO(fp.read())
        im = Image.open(img)

        #Resize the image
        im2 = im.resize((500, 100), Image.NEAREST)

        #NOTE, we're saving the image into a cStringIO object to avoid writing to disk
        out_im2 = cStringIO.StringIO()
        #You MUST specify the file type because there is no file name to discern it from
        im2.save(out_im2, 'PNG')

        #Now we connect to our s3 bucket and upload from memory
        #credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        conn = boto.connect_s3()

        #Connect to bucket and create key
        b = conn.get_bucket('backpackbuilder')
        k = b.new_key(title + '.png')

        #Note we're setting contents from the in-memory string provided by cStringIO
        k.set_contents_from_string(out_im2.getvalue())
