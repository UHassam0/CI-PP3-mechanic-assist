## Features

![flowchart](./flowchart.jpeg)

The concept here is that employees at a garage may want a program to help them maintain a list of customers. The tool could also remind them to contact customers and book in MOTs as they near the due date

I connect to a google sheet called. 'Mechanic-Customers', there is a tab/sheet called 'Customer-Information'. This is the storage colution for the customer and MOT information. The data is in columns headed: Name, Phone, Make, Model, Age, Mileage, Next MOT due, Booked Y/N. 

Some key aspects of the validation are as follows. The phone number must match standard uk numbers starting 01, 02 or 07 and having 11 digits. The car makes and models are validated against a spreadsheet found online, which, while comprehensive is in no way an official or infallible list. I have opted to only allow integers for the car age and to seek confirmation from the user where the mileage input doesn't approximately match the average for the age. I am using 10,000 miles as the widely accepted average mileage per year for cars. Next MOT due must be within the next year and in the future.
 
I want a user to be choose whether they are inputting one at a time, sharing a google sheet, or querying the information. I want to validate each input. I changed my mid along the way and have decided that there is no need for a program to append rows from 1 google sheet to another and this may be best to remain a manual and authorised process. This may be revisited of course and the basic data validation functions do exist already. There are 2 distinct aspects of the program wrapped in a looping input asking the customer to choose between entering data or querying the data

Where the customer chooses to input data it proceeds as a survey asking for the customer and vehicle information validating and feeding back at each step. Once all the information is collected the user is advised the the data is being added to the database and advised when complete. They then return to the main menu and may choose to input more data or query the data.
 
When querying the data I want to show the user several simple bits of information. Thes are: most popular car model, average age and average mileage. Perhaps more importantly, I also want the user to see a list of MOTs due in 8 weeks that are not yet booked. The user may then input the ID number of any customers MOTs they book in, which will update the spreadsheet. Alternatively, they may return to the main menu.


## Testing

Tested and passed through CI Python Linter

!['Linter passed image'](./CI%20lInter.png)

Also passed various input tests. I did this personally and tried many combinations of false inputs to ensure that they would be validated out and the feedback was helpful. My mentor also helped with this and in fact, it was him that pointed out the need to prevent blank space input for the customer name

After deployment I have noticed that where the age is 0 years i.e the car is brand new, the mileage validation feedback is a little skewed as 10,000 multiplied by 0 is still 0 - I could potentially use up to 10,000 miles as reference for 0 year age as a special case. However, as a specila case there is also no harm in double checking with the user anyway

I have also noticed that I could potentially add feedback when the user updates to indicate an MOT is booked in. It is not howver, a significant issue in the flow or user experience.

I have also omitted to update whether or not the MOT is booked in while inputting data

Initially, I had the input on the same line as the input query, however to deploy to heroku using the template provided it is necessary to add the new line. Both look and work similarly.

The feedback for incorrect phone numbers is lacking

## Deployment

Deployed to Heroku using love sandwiches instructions. Deployed well with no issues

## Credits

I found the sheet to validate car make and model data against here: https://www.carmodelslist.com/car-manufacturers/

Thank you to my mentor Jubril Akolade for his input and support and motivation