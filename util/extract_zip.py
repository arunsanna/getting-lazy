import zipfile
import zlib

src = open("/tmp/target.zip", "rb")
zf = zipfile.ZipFile('/tmp/target.zip')
for m in zf.infolist():

    # Examine the header
    print m.filename, m.header_offset, m.compress_size, repr(m.extra), repr(m.comment)
    src.seek( m.header_offset )
    src.read( 30 ) # Good to use struct to unpack this.
    nm= src.read( len(m.filename) )
    if len(m.extra) > 0: ex= src.read( len(m.extra) )
    if len(m.comment) > 0: cm= src.read( len(m.comment) )

    # Build a decompression object
    decomp= zlib.decompressobj(-15)

    # This can be done with a loop reading blocks
    out= open( m.filename, "wb" )
    result= decomp.decompress( src.read( m.compress_size ) )
    out.write( result )
    result = decomp.flush()
    out.write( result )
    # end of the loop
    out.close()

zf.close()
src.close()