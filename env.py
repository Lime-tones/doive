import os, sys, IPython
def install_vendors():
    
    print("Installing vendors -> ", end="")
    import os, IPython
    if os.path.exists("vendor/.installed"):
        print("Done.")
        return
    try:
       print("Done.")
    except Exception as e:
        print("Error: %s" % e)
