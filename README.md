# Alfred-Calendly - An Alfred Workflow for Calendly API v2

> This workflow is in `alpha` stage at the moment.

## Use Cases

### Requesting Single-Use-Links for Event Types

![alfred-calendly](single_use_link.gif)

*More to come*

## Build

1. Download or Clone this Repository

2. Run 

   ```sh
   $ make
   ```

3. Install `alfred-calendly.alfredworkflow`

## Initial Setup (OAuth flow)

1. Have the registration of a OAuth Client approved by Calendly.
   - This is only possible for Pro and Premium accounts.
   - Follow these instructions: https://calendly.stoplight.io/docs/api-docs/docs/A-API-Getting-Started.md#how-to-get-your-authentication-token
   - Wait for approval and your credentials (`Client ID` and `Client Secret`)

2. In Alfred, enter `cya` (Calendly Authentication) in order to setup your client.
   - Hit enter
   - Paste `Client_ID:Client_Secret` into Alfred Prompt, hit Enter

3. In Alfred,  enter `cya` again.
   - You will have to request an OAuth Authorization Code from Calendly. To do so, you need to log into you Premium Account of Calendly.
   - Just hit Enter again.
   - You will be redirected to Calendly.
   - Grant your client access to Caledly.
4. Upon grant, Calendly will redirect you to a yet broken url "https://www.calendly.sebwarnke.com", (this is to be improved). The URL carries an `auth_code` parameter.
   - Copy the `auth_code`
5. In Alfred, enter `cya`, once again
   - Hit Enter
   - Paste the `auth_code`
   - Hit Enter
   - Now you should have a registered client that can communicate with the API of Calendly.