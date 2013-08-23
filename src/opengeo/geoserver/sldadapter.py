def adaptQgsToGs(sld):
    sld = sld.replace("SvgParameter","CssParameter")
    sld = sld.replace("1.1.","1.0.")
    return sld

def adaptGsToQgs(sld):
    return sld