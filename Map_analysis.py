import arcpy
import os

arcpy.env.workspace = r"C:\GE\data\input"
arcpy.env.overwriteOutput = True

shapefiles = [shp for shp in arcpy.ListFeatureClasses() if shp.endswith('.shp')]

output_mxd = r"C:\GE\map\automated_map.mxd"
output_pdf = r"C:\GE\Output_map\islamicUniversity.pdf"

template_mxd = r"C:\GE\data\templates\blank_map.mxd"
mxd = arcpy.mapping.MapDocument(template_mxd)
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

def add_layer(layer_path, data_frame):
    try:
        layer = arcpy.mapping.Layer(layer_path)
        arcpy.mapping.AddLayer(data_frame, layer, "TOP")
        print("Layer added: {}".format(os.path.basename(layer_path)))
    except Exception as e:
        print("Failed to add layer {}: {}".format(os.path.basename(layer_path), str(e)))

def apply_labels(layer_name):
    try:
        layer = arcpy.mapping.ListLayers(mxd, layer_name, df)[0]
        layer.showLabels = True
        label_class = layer.labelClasses[0]
        label_class.expression = "[NAME]"  # Change this based on your attribute field for labels
        print("Labels applied to layer: {}".format(layer.name))
    except Exception as e:
        print("Failed to apply labels for {}: {}".format(layer_name, str(e)))

for shp in shapefiles:
    layer_path = os.path.join(arcpy.env.workspace, shp)
    add_layer(layer_path, df)
    apply_labels(os.path.basename(shp).replace(".shp", ""))  # Apply labels based on the layer name

try:
    arcpy.mapping.ExportToPDF(mxd, output_pdf)
    print("Map exported to PDF: {}".format(output_pdf))
except Exception as e:
    print("Failed to export map to PDF: {}".format(str(e)))

try:
    mxd.saveACopy(output_mxd)
    print("Map document saved: {}".format(output_mxd))
except Exception as e:
    print("Failed to save map document: {}".format(str(e)))

del mxd
