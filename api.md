
 GET /getBook
     
   headers:
    
          api_key : "secret key"

   paramets :
    
         limit (default 10)
         author
         category
         cursor (optional)

   response : 
    
          {
            "books" : [
                         "id" : {
                             "name" : "harry potter"
                             "author" : "JK"
                             "category": "friction"
                          }
                      ]
           "cursor": "xdfsjlkdfjkldf"
          }

POST /addBook
  
   headers : 
        
        Content-type : application/json, api_key : "secret key"
    
   payload :
         
        { "name" : "harry potter", "author": "JK", "category" : "friction"}

   response : 
   
         { "success": true }
