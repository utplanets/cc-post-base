rule decompile_namelist:
  output: "output/namelist.decompiled"
  input: "../namelist.input"
  shell:"""
  pwrf namelist decompile {input} -o {output}
"""