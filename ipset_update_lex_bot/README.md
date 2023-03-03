1-  In the bot defintion, there is a section
``` "slotTypes": [
      {
        "description": "instance id to create snapshot of",
        "name": "ipsetName",
        "version": "1",
        "enumerationValues": [
          {
            "value": "test",
            "synonyms": []
          }
        ],
        "valueSelectionStrategy": "ORIGINAL_VALUE"
      },
      {
        "name": "ip",
        "version": "1",
        "enumerationValues": [
          {
            "value": "10.0.0.0",
            "synonyms": []
          }
        ],
        "valueSelectionStrategy": "ORIGINAL_VALUE"
      }
    ], ```
Here you need to name matching your IPSet name and add values for IPv6 format also.

2-  Import the definition using Lex V1 console.

3-  Grant Lex permisison to invoke Lambda
  
  ``` aws lambda add-permission --function-name ipset_validation --statement-id chatbot-fulfillment1 --action "lambda:InvokeFunction" --principal "lex.amazonaws.com" --region us-west-2
  aws lambda add-permission --function-name ipset_fulfilment --statement-id chatbot-fulfillment2 --action "lambda:InvokeFunction" --principal "lex.amazonaws.com" --region us-west-2 ```
  
4-Follow Step2 to Step6 given at https://docs.aws.amazon.com/lex/latest/dg/slack-bot-association.html to create a Slack application that integrates with our Lex bot.
