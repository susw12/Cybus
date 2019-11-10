<h1 align="center">
 <img src="https://github.com/susw12/teenhacksli/blob/master/Logo.png" width="300">
 <br>
 Cibus
 <br>
</h1>

## Inspiration
The eating habits of college students is a very well documented issue. Over the summer I was taking a course at Harvard University, and as a part of the program, we had to find our lunches daily. There were several college students in my class, and after discussing their normal dietary habits with them, I realized that many college students defaulted to fast-food restaurants, due to their convenience, in time, cost, and proximity. 

Interested in this issue, we conducted further research. According to a study conducted by researchers at Vrije Universiteit Brussel and Ghent University in Brussels, Belgium, college students' dietary habits are heavily affected by their personal preference, their peer groups, their physical environment, and the media that they consume. [\[1\]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3905922/) Another study conducted by researchers at the University of Parma in Parma, Italy, Cornell University in Ithaca, New York, and EGADE Business School in San Pedro Garza García, Mexico, found that students would prefer low-cost, unhealthy options due to their taste and convenience. Additionally, they found that many students actively avoided preparing their meals, due to cost and time constraints. However, those students who were able to cook their food were noticeably healthier. [\[2\]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6315356/) 

As we talked with college students who lived in our area, we realized that many of the students, especially the ones who were not from the area, did not know many of the local grocery stores and farmers' markets in the area. One student we talked to at the University of Maryland, College Park, mentioned that even though he was from the Maryland area, he still had no clue about the local stores near and on the university campus. However, local grocery stores and farmers' markets provide healthier and tastier foods and lower costs, while supporting the local economy. [\[3\]](https://www.besthealthmag.ca/best-eats/healthy-eating/20-benefits-of-shopping-at-a-farmers-market-vs-the-supermarket/) 

As a result of the issues that we had come across, we wanted to make an application that would enable every student, regardless of how busy they were, their dietary restrictions, or their socio-economic status, be able to have healthy, homecooked meals that would promote healthy eating habits for a low cost while connecting them with local grocery stores and farmers markets, to help promote local business and foster a sense of community among the students and residents.

## What it does
Our website and mobile app allow college students to find recipes, places to buy ingredients, nutrition facts, costs and plan their meal plan. It also allows local businesses to post listings about the products that they have available and advertise their business.

The student portal of our application is targeted towards students who are living in off-campus settings where they have access to basic kitchen equipment. There is also a feature for students who are living with roommates that allow students to create groups with the people that they are living with. This provides an announcement feed and a message board-style posting platform where roommates can post-meal plans, interesting recipes, etc. The recipes tab provides the students with access to over 350,000 recipes for them to choose from. Students can filter their meals based on dietary restrictions, such as nut allergies, vegetarianism, lactose intolerance, etc. Each recipe entry also contains nutritional information, like calories per serving, serving size, fat, carbohydrates, etc. The ingredients tab provides students with a search platform where they can find stores that have what they want, the cheapest place to buy the items, and nutritional facts about the different food that they want to purchase.

The company page contains an information tab that allows local stores to provide information about their company, similar to an about page. The products tab allows the stores to post their products that they are carrying, like tomatoes, cucumbers, meats, etc., and the costs of these products.

## How we built it
Our app is built using a Flask webserver to handle our backend interactions, like webpage management, data handling, and GET and POST functions. We are using an SQLite3 database to manage our data, including announcements, store listings, etc. We are using Edamam's Recipe Search API and Food Database API for our recipes and nutritional value for the ingredients, respectively. We used Bootstrap's CSS and JS library, combined with several Bootstrap templates for our frontend. Our website is hosted on a Google Cloud Console instance running Ubuntu 18.04 LTS server.
