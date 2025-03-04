# Creating transcriptions and search process for video files

Slice large video

```sh
# slice long video into 1h (3600s) segments, can't be longer than 4h, 2 digits pattern
ffmpeg -i "my_large_file.mp4" -c copy -map 0 -segment_time 3600 -f segment -reset_timestamps 1 my_file_%02d.mp4
```

```sh
export VIDEO_DIR='~/videos/'
export VIDEO_BUCKET='s3://your-bucket/videos/'

# copy files to s3 bucket, you can also use aws s3 cp
aws s3 sync $VIDEO_DIR$ s3://$VIDEO_BUCKET --exclude "*" --include "*.mp4"

# start transcription job
aws transcribe start-transcription-job \
  --transcription-job-name "ZoomMeetingTranscript" \
  --media MediaFileUri=s3://your-bucket/your-zoom-recording.mp4 \
  --language-code "en-US" \
  --output-bucket-name your-output-bucket

# check a specific transcription job status
aws transcribe get-transcription-job --transcription-job-name "ZoomMeetingTranscript"
# or all jobs that are running
aws transcribe list-transcription-jobs --status IN_PROGRESS
# {
#     "Status": "IN_PROGRESS",
#     "TranscriptionJobSummaries": [
#         {
#             "TranscriptionJobName": "2025-02-25-2",
#             "CreationTime": 1740561128.431,
#             "StartTime": 1740561128.448,
#             "LanguageCode": "en-US",
#             "TranscriptionJobStatus": "IN_PROGRESS",
#             "OutputLocationType": "CUSTOMER_BUCKET"
#         },
#         {
#             "TranscriptionJobName": "2025-02-25-1",
#             "CreationTime": 1740561079.061,
#             "StartTime": 1740561079.09,
#             "LanguageCode": "en-US",
#             "TranscriptionJobStatus": "IN_PROGRESS",
#             "OutputLocationType": "CUSTOMER_BUCKET"
#         }
#     ]
# }

# download files for postprocessing
aws s3 sync s3://$VIDEO_BUCKET $VIDEO_DIR --exclude "*" --include "*.json"
# convert transcriptions into srt
python ./convert_transcribe_json_to_srt.py my_file.json my_file.srt
```

## Search for text


```sh
python ./search_srt.py my_file.json my_file.srt
```
