function handler(event) {
    var request = event.request;
    var headers = request.headers;
    var host = headers['host'].value;
    var uri = request.uri;
    var lowercaseUri = uri.toLowerCase();
    if (uri !== lowercaseUri) {
        var redirectUrl = "https://" + host + lowercaseUri;
        
        var response = {
            statusCode: 301,
            statusDescription: 'Moved Permanently',
            headers: {
                location: {
                    value: redirectUrl
                }
            }
        };
        
        return response;
    }
    
    return request;
}


# curl -L https://d1cd8.cloudfront.net/Secondbucket will redirect to https://d1cd8.cloudfront.net/secondbucket
