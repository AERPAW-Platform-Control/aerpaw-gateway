import geni.util
import geni.aggregate.cloudlab

context = geni.util.loadContext(key_passphrase="exogeni@4516")
print(context.cf.key)
print(context.cf.cert)
#print(geni.aggregate.cloudlab.Renci.getversion(context))
ad=geni.aggregate.cloudlab.Renci.listresources(context)
#print(ad.text)
ad=geni.aggregate.cloudlab.Renci.listresources(context,"urn:publicid:IDN+exogeni.net:testproject1+slice+erikaadm-QV113")
print(ad.text)