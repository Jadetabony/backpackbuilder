import boto
import cStringIO
import urllib
from PIL import Image
from pymongo import MongoClient


def imageLinkToS3(image_link, image_title, s3_connection):
    """Takes a image from the given link and stores it in the identified S3 bucket.

    This function opens a URL that is provided by the user with urllib, formats
    it as a PNG file and then stores it in the connected S3 bucket.

    Attributes:
        image_link (string): Link to REI image in REI media files.

        image_title (string): Title for the image as it will be stored in S3 bucket.

        s3_connection (boto connection): Connection to the appropriate S3 bucket using boto library.

    TODO:
        * There has to be a better way to access all of the links.

    """

    fp = urllib.urlopen(image_link)
    # Load the URL data into an image
    img = cStringIO.StringIO(fp.read())
    im = Image.open(img)
    # Resize the image
    im2 = im.resize((500, 100), Image.NEAREST)
    #  we're saving the image into a cStringIO object to avoid writing to disk
    out_im2 = cStringIO.StringIO()
    # You MUST specify the file type because there is no file name to discern it from
    im2.save(out_im2, 'PNG')
    # Now we connect to our s3 bucket and upload from memory
    # credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    k = s3_connection.new_key(image_title + '.png')
    # Note we're setting contents from the in-memory string provided by cStringIO
    k.set_contents_from_string(out_im2.getvalue())


if __name__ == '__main__':
    client = MongoClient()
    db = client.products
    rei = db.rei

    conn = boto.connect_s3()
    # Connect to bucket and create key
    b = conn.get_bucket('backpackbuilder')

    for entries in rei.find({}):
        title = entries['title']
        print title
        links = entries['img_list']
        print links
        for url in links:
            imageLinkToS3(url, title, b)
