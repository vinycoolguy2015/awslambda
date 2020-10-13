
import boto.ec2

# Read the public key material from the file
fp = open('C:\\Users\\vinayak.p\\Documents\\id_rsa.pub')
material = fp.read()
fp.close()
regions = boto.ec2.regions()
for region in regions:
    try:
        connection=boto.ec2.connect_to_region(region.name,aws_access_key_id='',aws_secret_access_key='')
        try:
            connection.import_key_pair('mykey', material)
        except boto.exception.EC2ResponseError,e:
            if e.code=="InvalidKeyPair.Duplicate":
                print e.message
            else:
                raise
        
    except  boto.exception.EC2ResponseError,e:
            if e.code=="AuthFailure":
                print e.message
            else:
                raise
        
        
                                    
