# Token Studio

A beginner-friendly Flask app that creates a labeled identification token through a responsive web form or a JSON API. Tokens are generated with Python's `secrets` module, which is designed for unpredictable values.

## Project files

- `app.py` — Flask page and token API, input validation, and JSON HTTP errors.
- `templates/index.html` — accessible HTML form and token result display.
- `static/app.js` — submits the form without a page reload and handles success, errors, and copying.
- `static/style.css` — responsive visual styling.
- `tests/test_app.py` — automated tests for the page and API behavior.
- `requirements.txt` — Python package dependencies.

## Run in GitHub Codespaces

1. Open the repository in a Codespace and open its terminal.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install Flask:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. In the **Ports** tab, open forwarded port `5000` in the browser. Enter a label and select **Generate token**.

The server listens on `0.0.0.0` and port `5000` by default, so Codespaces can forward it. Set `PORT` to use another port. For local development only, set `FLASK_DEBUG=1` to enable Flask debug mode.

## Test

Run the unit tests from the `python-token-app` directory:

```bash
python -m unittest discover -s tests -v
```

## API

`POST /api/token` accepts a JSON object with a non-empty `label` of at most 100 characters:

```json
{
  "label": "staging environment"
}
```

A successful request returns HTTP `201`:

```json
{
  "success": true,
  "label": "staging environment",
  "token": "a-url-safe-token"
}
```

Validation and request-format errors return a JSON object with `success: false` and an `error` message. For example, test the endpoint in Postman by sending a `POST` to `https://<your-codespace>-5000.app.github.dev/api/token` with `Content-Type: application/json` and the request body above. The exact forwarded URL appears in the Codespaces **Ports** tab.

The generated token is an identifier for this demo; the app does not store tokens or associate them with accounts.
