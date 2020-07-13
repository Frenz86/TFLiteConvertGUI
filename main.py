
from guietta import _ , Gui , R1 , R2 , QFileDialog
import os

app = Gui(
    [ "TFLiteGUI : A GUI utility to convert frozen graphs, checkpoints, saved models to TFLite models." ],
    [ "Convert from" ],
    [ R1( "Frozen graph ( .pb )") , R1( "Keras model ( .h5 )" ) , R1( "Saved Model" ) ],
    [ "Resource path ( Path to the frozen graph, checkpoints/saved model directory ) :"  ],
    [ "__path__" ],
    [ [ 'Browse' ] , _ , _ ],
    [ "Input array names ( comma separated )"  ],
    [ "__inputs__" ],
    [ "Output array names ( comma separated )"  ],
    [ "__outputs__" ],
    [ "Inference type" ],
    [ R2( "FLOAT") , R2( "QUANTIZED_UINT8") , _ ],
    [ "Mean and Standard Deviations values ( mean_value , std_dev_value ) ( Only if inference type is QUANTIZIED_UINT8 ) " ],
    [ "__mean_std__" ],
    [ "Input shapes" ],
    [ "__input_shape__" ],
    [ "Output file" ],
    [ "__output_path__" ],
    [ "Additional Commands" ],
    [ "__commands__" ],
    [ "" ],
    [ [ 'Convert To TFLite' ]  , [ 'Clear All' ] , _ ]
)

def clear_all(gui, *args):
    app.path = ""
    app.inputs = ""
    app.outputs = ""
    app.mean_std = ""
    app.input_shape = ""
    app.commands = ""
    app.output_path = ""
app.ClearAll = clear_all

def open_file(gui, *args):
    filename = QFileDialog.getOpenFileName(None, "Choose file" )
    app.path = filename[0]
app.Browse = open_file

with app.ConvertToTFLite:
    command = ""
    inputCommand = "--graph_def_file"
    if app.Frozengraphpb.isChecked():
        inputCommand = "--graph_def_file"
    elif app.Kerasmodelh5.isChecked() :
        inputCommand = "--keras_model_file"
    elif app.SavedModel.isChecked():
        inputCommand = "--saved_model_dir"
    command += "{}={} ".format(inputCommand, app.path)

    command += "--output_file={} ".format(app.output_path)
    command += "--input_arrays={} --output_arrays={} ".format(app.inputs, app.outputs)

    inferenceType = 'FLOAT'
    if app.FLOAT.isChecked():
        inferenceType = 'FLOAT'
    else:
        inferenceType = 'QUANTIZED_UINT8'
    command += "--inference_type={} ".format(inferenceType)

    if inferenceType == 'QUANTIZED_UINT8':
        command += "--mean_values={} --std_dev_values={} ".format(app.mean_std.split( ',' )[0].strip(),
                                                                  app.mean_std.split( ',' )[1].strip())
    if app.input_shape.strip() != '':
        command += "--input_shapes={} ".format(app.input_shape)

    command += app.commands
    command = 'tflite_convert ' + command

    os.system( 'echo {}'.format( "TFLiteConvertGUICommand " + command ))
    os.system( command )

app.window().setWindowTitle( 'TFLiteConvertGUI' )
app.run()

