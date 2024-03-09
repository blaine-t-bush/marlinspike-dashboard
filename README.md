# marlinspike-dashboard

Dashboard for displaying location-specific weather and public transport data

## Development

To run with docker, first copy `.env.example` to `.env` and change latitude and longitude to your desired location,
then build and run the image:

```bash
docker build -f Dockerfile -t dashboard .
docker run -p 5000:5000 dashboard
```

Then visit `localhost:5000` in your browser.
