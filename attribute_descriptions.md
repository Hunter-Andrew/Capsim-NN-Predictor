# Attribute Descriptions

**Name**: Name of the product

**Market Share**: Market share of the product in the segment specified by the Tech attribute during the whole year.

**Units Sold**: Very similar to market share, same constraints, but represented as units sold.

**Revision Date**: Date of completion of last revision to the product. Note that the product's age, pfmn, size, MTBF, and instantaneous CSS are likely to change after this revision.

**Stock Out**: 1 if the product sold out at sometime throughout the year, otherwise 0.

**Pfmn**: The product's performance, which is proportional to the quality of the product.

**Size**: The product's size, which is inversely proportional to the quality of the product.

**Position Difference**: The (absolute value) difference between the product's position and the instantaneous idea position for the specified segment (each segment has a different ideal position). 
Note that a product's position is the 2d vector (pfmn, size). A position difference of 0 is ideal.

**Price**: The product's price.

**Price Difference**: Difference between product price and ideal price (specific to segment), where a negative value means that the product price is lower than the ideal price. Since I'm not sure how the 
price score is calculated (see Price Score above), I'm not going to help the algorithm as much as I have on other scores (like MTBF score). However, I do think that I should incorporate the ideal 
price (lower bound of the range), because otherwise, the model will have to use theTech attribute in combination with the price attribute to accurately see how the price affects the CSS. Instead, 
I think it'd be easier to learn that a positive price difference close to zero is good (for CSS), and a negative price difference may or may not be bad.

**MTBF**: The product's reliability, which is proportional to the product's performance, except any MTBF above the ideal MTBF is equivalent quality.

**MTBF Score**: The difference between the product's MTBF and the ideal MTBF specific to the segment (each segment has a different ideal MTBF). A score of 0 is ideal. Any MTBF better than the ideal MTBF 
still has score 0.

**Age**: The age of the product. Note that any time a product is revised, it's age is divided by 2.

**Age Difference**: The difference between the product's age and the ideal age specific to the segment (ideal age for low tech is 3, ideal age for high tech is 0). The ideal age difference is 0.

**Promo Budget**: How much money was spent on product promotion.

**Cust. Aware.**: Percentage of customers aware of the product. Depends on promo budget, and customer awareness from last year.

**Sales Budget**: How much money was spent on sales. 

**Cust. Acces.**: How accessible the product is. Depends on sales budget and customer accessibility from last year.

**Segment**: 0 if the tuple is from the low tech segment analysis. 1 if tuple is from the high tech segment. Note that different segments have different ideal values for many important attributes 
(attributes that CSS depnds on), making this attribute one of the most important attributes to predict CSS. For example, if you were given all other attributes except which segement the product was 
targetting, there would be 2 answers (a CSS for the low tech segment, and a CSS for the high tech segment). However, as part of the pre-processing/augmentation, the attributes affected by the 
segment the tuple is from is adjusted to be the difference between the segment's ideal value, and the actual attribute value. This helps the model learn immensely, but it also makes the entropy of 
this attribute quite high (theoretically entropy of this attribute should be 1).

**Current Round**: The simulation consists of 8 rounds (simulated years). The round number is the round that the tuple is from.

**Position Out of Range**: Based on instructions from Capsim, the CSS will be more heavily penalized if the position is more than 4 units away from the ideal position. This attribute will be 1 if this 
penalization occurs, and 0 otherwise.

**Price Out of Range**: Based on instructions from Capsim, the CSS will be more heavily penalized if the price is more than $20 away from the ideal price. This attribute will be 1 if this 
penalization occurs, and 0 otherwise.

**MTBF Out of Range**: Based on instructions from Capsim, the CSS will be more heavily penalized if the MTBF is more than 6000 units away from the ideal MTBF. This attribute will be 1 if this 
penalization occurs, and 0 otherwise.

**Age Out of Range**: Based on instructions from Capsim, the CSS will be more heavily penalized if the age is more than 1 year away from the ideal position. This attribute will be 1 if this 
penalization occurs, and 0 otherwise.

**CSS**: Target attribute. Instantaneous rating of the product. Specific to the segment, as different segments have different ideals. 
