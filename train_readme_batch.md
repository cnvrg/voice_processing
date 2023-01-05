You can use this blueprint to convert speech to text using your own voice sample. In order to get the result in your desired language and desired accuracy you will be needed to provide: --speech audio file uploaded by the user on the platform --language language the user wants the text to be transcribed/translated in --model_size size of the model the user wants to use so as to create a balance between accuracy and time consumed 

You would need to provide 1 folder in s3 where you can keep your voice sample or you can directly supply a youtube link to the audio file but you need to supply the link in double quotes otherwise the arguments get confused with the special characters in the youtube link and the blueprint fails

voice_processing: Folder containing the voice sample "audio.wav"
Directions for use:

Click on Use Blueprint button

You will be redirected to your blueprint flow page

In the flow, edit the following tasks to provide your data:

In the S3 Connector task:

Under the bucketname parameter provide the bucket name of the data
Under the prefix parameter provide the main path to where the input file is located
In the Data-Preprocessing task:

Under the raw_train_data parameter provide the path to the input folder including the prefix you provided in the S3 Connector, it should look like: /input/s3_connector/<prefix>/<prefix>.wav
NOTE: You can use prebuilt data examples paths that are already provided

Click on the 'Run Flow' button
In a few minutes you will train a new rul model and deploy as a new API endpoint
Go to the 'Serving' tab in the project and look for your endpoint
You can use the Try it Live section with a data point similar to your input data (in terms of variables and data types) to check your model
You can also integrate your API with your code using the integration panel at the bottom of the page
Congrats! You have trained and deployed a custom model that detects the number of cycles under which the machine is going to fail