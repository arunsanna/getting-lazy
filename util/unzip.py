import zipfile
zip_ref = zipfile.ZipFile('', 'r')
zip_ref.extractall('/tmp/')
zip_ref.close()