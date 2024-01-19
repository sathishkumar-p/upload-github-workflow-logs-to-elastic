# Upload Logs to Openseach

This action provides the functionality to upload the GitHub action workflow run logs to Opensearch. 

# Usage

See [action.yml](https://github.com/sathishkumar-p/upload-github-workflow-logs-to-opensearch/blob/main/action.yml)

```yml
upload-logs-to-opensearch:
    name: "Upload Logs to Opensearch" 
    runs-on: [ ubuntu ]
    needs: deploy
    if: ${{ !cancelled() && (success() || failure() || needs.deploy.result == 'skipped') }}
    steps:    
      - name: Upload GitHub Action workflow logs to Opensearch
        uses: sathishkumar-p/upload-github-workflow-logs-to-opensearch@v6
        with:
          # Github PAT Token access to workflow logs
          github_token: "${{ secrets.PAT }}"
          # Github organization name 
          github_org: "ABC"
          # Github repository name
          github_repository: "my-abc"
          # Github workflow run id 
          github_run_id: "${{ github.run_id }}"
          # Github API URL to collect the logs.
          # For Public Github Free, Pro & Team. URL is https://api.github.com
          # For self-hosted or Enterprise Version. URL is https://<<Enterprise Host>>/api/<<api version>>
          github_host_api: "https://api.github.com"
          # Opensearch is enabled with HTTP basic auth username and password required
          opensearch_username: "${{ secrets.OPENSEARCH_USERNAME }}"
          opensearch_password: "${{ secrets.OPENSEARCH_PASSWORD }}"
          # Opensearch Host URL. Example : https://openseach:443
          opensearch_host: "${{ vars.OPENSEARCH_HOST }}"
          # Opensearch index pattern name
          opensearch_index: "ci-cd"
```

&nbsp;
