
 GET /Book
 
  request:
     
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
                         {   "id":  1441041
                             "name" : "harry potter"
                             "author" : "JK"
                             "category": "friction"
                          }
                      ]
           "cursor": "xdfsjlkdfjkldf"
           "more": true
          }

POST /Book
   
   request:

      headers : 

           Content-type : application/json, api_key : "secret key"

      payload :

           { "name" : "harry potter", "author": "JK", "category" : "friction"}

   response : 
   
         { "success": true, id: 43243-5253098-ldslf }
         
 PUT /Book/< id >
    
   request:

      headers : 

           Content-type : application/json, api_key : "secret key"

      payload :

           { "name" : "harry potter", "author": "JK", "category" : "friction"}

   response : 
   
         { "success": true, id: 43243-5253098-ldslf }
         
         
 DELETE /Book/< id >
    
   request:

      headers : 

          api_key : "secret key"

   response : 
   
         { "success": true, id: 43243-5253098-ldslf }
    
    
    
         
         
post /requestbook

   request:
        
     headers :
        
          content-type : application/json, api_key : "secret key"
          
     payload :
       
          {"bookname": "And then they were none ", "author": "Agatha Cristie"}
          
    response :
      
          {'success": true }
              
