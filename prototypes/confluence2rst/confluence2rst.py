from JumpScale import j
j.application.start('confluence2rst')

import JumpScale.portal.docgenerator
import lib.objectinspector


# ignore = ["zredisgw"]
# dest = "/opt/code/github/jumpscale/generated_docs/docs/source/API/"
# j.tools.objectinspector.generateDocs(dest, ignore)

src = "/opt/code/github/jumpscale/jumpscale_docs/Spaces/"
dst = "/opt/code/github/jumpscale/generated_docs/docs/source/spaces"
j.tools.docgenerator.convertConfluenceToRST(src, dst)

j.application.stop()