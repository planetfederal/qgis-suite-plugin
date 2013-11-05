def importToPostGIS(explorer, connection, toImport, schema, tablename, add, single):
    if len(toImport) > 1:
        explorer.setProgressMaximum(len(toImport), "Import layers into PostGIS")           
    for i, layer in enumerate(toImport):  
        explorer.setProgress(i)                  
        if not explorer.run(connection.importFileOrLayer, 
                            None, 
                            [],
                            layer, schema, tablename, not add, single):
            break                                            
    explorer.resetActivity()  