# Alfred-Calendly - An Alfred Workflow for Calendly API v2

## Use Cases

### Requesting Single-Use-Links for Event Types

![alfred-calendly](single_use_link.gif)

*More to come*

## Prerequisites

- To use this workflow you need a payed Calendly subscription.
- Have a Oauth client registered at Calendly. To do so, follow [these steps](https://calendly.stoplight.io/docs/api-docs/docs/A-API-Getting-Started.md#how-to-get-your-authentication-token).
- You need to provide Calendly with a Redirect URI which they use to call you back with an Authorization Token. You can use `http://localhost` or anything more meaningful to your use case. But keep this URI for the following configuration of the workflow.
- As a result of the registration, Calendly will provide you with some initial credentials. You need them to configure the workflow:
  - Oauth Client ID
  - Oauth Client Secret

## Installation

1. Download the latest release of the workflow [here](https://github.com/sebwarnke/alfred-calendly/releases).
2. Install workflow.
3. In Alfred, enter `cya` and follow the instructions to start the Oauth authorization flow.
   - You need to enter your Client ID and Client Secret here.
   - The workflow expects the following format: `<CLIENT_ID>:<CLIENT_SECRET>`. Mind the delimitting colon!
4. In Alfred, enter `cya` again, and follow the instructions to enter the Redirect URI.
   - The URI needs to comply with the URI you've provided Calendly with during registration of the client.
   - Dont forget `http[s]://` in the URI.
5. In Alfred, enter `cya` again, follow the instructions to authorize the workflow towards Calendly.
   - This opens Calendly in a Web Browser. Follow the instructions there.
   - In the end you will be redirected to your redirect uri.
6. From the Redirect URL, copy the value of the `code` get-parameter. This is your Authorization Code,
7. In Alfred, enter `cya` once more and follow the instructions. You will be asked to paste the Authorization Code received in step 6.
8. Congratulations, you've passed the Oauth flow.

### I did some thing wrong!

No worries, just call `cya reset` to start from step 3. again.

## Build it your own

1. Download or clone this repository

2. Enter directory and call

   ```
   $ make && open -a Alfred\ 4 Alfred-Calendly.alfredworkflow
   ```

   