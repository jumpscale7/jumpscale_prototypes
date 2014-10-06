from JumpScale import j
j.application.start('confluence2rst')

import JumpScale.portal.docgenerator
import lib.objectinspector


ignore=["zredisgw", "ipshell"]
dest="/opt/code/github/jumpscale/jumpscale_docs/Spaces/Doc_Jumpscale_Libraries/Docs/"
j.tools.objectinspector.generateDocs(dest,ignore)

src = "/opt/code/github/jumpscale/jumpscale_docs/Spaces/"
dst = "/opt/code/github/jumpscale/generated_docs/docs/_source/spaces"
j.tools.docgenerator.convertConfluenceToRST(src, dst)

j.application.stop()
