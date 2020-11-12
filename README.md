# Auction-website_Python
Its a simple auction site developed by using Django framework.
List of ImplementedTask:
UC1 Create user Account:It has been completed and working fully functional.
UC2Edituser Account:Web application has the ability to update the account information email and password of the signed in user.
UC3Create an Auction:Application has the functionality to create new auction if the user is logged in. otherwise visitor can only see all the available auctions which are not banned.
Optional Features:
System will automatically send the email to the user when the new auction created with the link of that auction.
Seller can edit the information of the auctions which he owns.
Other logged in user can bid for the auction but not the seller.
Administrator can ban any auction.
When auction created it will re direct to the new page with message of confirmation that auction has been created
If the title already exist it gives an error that it already exist.
UC4Edit anAuction:Application has the functionality to edit the information given foranauction while it was created.
UC5Browse and Search Auction:Both the functionalitiesare working perfectly in searching and browsingwiththe titleof auction.
UC6BidforanAuction:All the required task for this functionalityis working but didn’timplement email and optional feature in it. Email is working when we createnewauction.
7.UC7BananAuction:This functionality has been implemented and is in working condition.Admin can ban the auction, seller can see his banned auction but the other users will not be able to see the banned auctions when they click “All Auction”.
UC8ResolveanAuction:This task is not implemented in the application.
UC9select Multiple Languages:This feature is also implemented and working perfectly, and it has 3 options for languages. English, Finnish and Swedish.
UC10 Concurrent Session:If the auction is in edit phase then other user will not be able to access it until editingis saved.
UC11Currency Conversion:This task is not implemented in the application.
UC12 Searching:This Functionality has been implement with RESTFUL webserviceand it’s fully functional.
UC13 Bidding:This Functionality has been implement with RESTFUL webserviceand it’s fully functional.

Confirmation of UC3:Confirmation form for new auction is not created but it will show the message to the new page that auction has been created.UC8 Resolving the Bids:This functionality is not implemented in the application.Concurrency in UC6:-Ihave the function request.user.is_authenticated() to now is he able to bid or not.-Then matched itwith the owner of the auction if they are same then its not able to bid.-If it’s user not the owner then it’s able to bid.-If it’s super user then it is also able bid for the auctionRestful Functionality:Yes, the application is the restful webservice for searching and bidding-Bidding: Hit with the URL http://127.0.0.1:8000/api/bid/auction/and pass the JSON with the parameters
