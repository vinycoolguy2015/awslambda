
1- In bot definition, replace <AWS_ACCOUNT_ID> with your account id.

2-  Import the definition using Lex V1 console.

3-  Grant Lex permisison to invoke Lambda
  ```
  aws lambda add-permission --function-name waf_validation --statement-id chatbot-fulfillment1 --action "lambda:InvokeFunction" --principal "lex.amazonaws.com" --region us-west-2
  aws lambda add-permission --function-name waf_fulfilment --statement-id chatbot-fulfillment2 --action "lambda:InvokeFunction" --principal "lex.amazonaws.com" --region us-west-2
  
  ```
  
4-Change handler name in Lambda configuration.

6-Follow Step2 to Step6 given at https://docs.aws.amazon.com/lex/latest/dg/slack-bot-association.html to create a Slack application that integrates with our Lex bot.
