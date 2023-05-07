"""
By: Andrew Hunter
Date: May 7, 2023

This file handles creating a 2d numpy array that represents the dataset. 

This dataset is used in predict_css.py. 

This dataset can be extracted from an input text file with a specific 
format. It can also be extracted from a csv file with a specific format. 

This dataset can also be exported to a csv file.
"""

import csv
import math

import numpy as np


class ExtractData:
    def __init__(self):
        """Initializes the dataset and attribute headers"""
        self.dataset = np.empty((0, 25))

    @staticmethod
    def get_headers():
        """Returns list of attribute names"""
        return [
            "Name",
            "Market Share",
            "Units Sold",
            "Last Revision Date",
            "Stock Out",
            "Pfmn",
            "Size",
            "Position Difference",
            "Price",
            "Price Difference",
            "MTBF",
            "MTBF Difference",
            "Age",
            "Age Difference",
            "Promo Budget",
            "Customer Awareness",
            "Sales Budget",
            "Customer Accessibility",
            "Segment",
            "Round",
            "Position Out of Range",
            "Price Out of Range",
            "MTBF Out of Range",
            "Age Out of Range",
            "CSS",
        ]

    def load_dataset(self, input_file):
        """Loads dataset from previously saved dataset saved/written to
        a csv file.

        Note that if the input csv file doesn't meet the correct format
        requirements, an error will likely occur.

        Note that if the input file contains headers (attribute names), 
        then the header row will not be included in the dataset.
        """
        # Clear dataset
        self.dataset = np.empty((0, 25))

        with open(input_file, "r", newline="") as f:
            reader = csv.reader(f)
            for i in reader:
                # If the row isn't headers (attribute names)
                if not i[0] in self.get_headers():
                    self.dataset = np.vstack((self.dataset, i))

    def _get_position_diff(
        self, curr_pfmn: float, curr_size: float, curr_round: float, segment: str
    ):
        """Returns the position difference. A low difference is
        better. Also returns true if the differnce is greater than 4,
        and false otherwise.

        A product's position is the 2d vector: (pfmn, size).

        The ideal pfmn and size is dependent on the round, and segment
        (low tech vs high tech).
        """
        if segment == 0:
            ideal_pfmn = 4.8 + 0.5 * curr_round
            ideal_size = 15.2 - 0.5 * curr_round
        else:
            ideal_pfmn = 7.4 + 0.7 * curr_round
            ideal_size = 12.6 - 0.7 * curr_round

        diff = math.hypot(curr_pfmn - ideal_pfmn, curr_size - ideal_size)

        if diff >= 4:
            return diff, 1
        else:
            return diff, 0

    def _get_price_score(self, price: float, segment: str):
        """Difference between product price and ideal price (specific
        to segment), where a negative value means that the product
        price is lower than the ideal price.

        Also returns 1 if the differnce is greater than 20,
        and 0 otherwise.
        """
        if segment == 0:
            diff = price - 15
        else:
            diff = price - 25

        if diff >= 20:
            return diff, 1
        else:
            return diff, 0

    def _get_MTBF_score(self, mtbf: int, segment: str):
        """Returns MTBF score depending on product's MTBF and the
        ideal MTBF for that segment (low tech vs high tech). MTBF
        represents the product's reliability.

        Any MTBF above the ideal MTBF has no benefit, and is equivalent
        to if the MTBF has equal to the ideal MTBF.

        Also returns true if the differnce is greater than 6000,
        and false otherwise.
        """
        if segment == 0:
            diff = 20000 - mtbf
        else:
            diff = 23000 - mtbf
        diff = max(0, diff)

        if diff >= 6000:
            return diff, 1
        else:
            return diff, 0

    def _get_age_diff(self, age: float, segment: str):
        """Returns the age difference between the product's age, and
        the ideal age for the segment. Wether or not the difference is
        greater than 1 is also returned, since it might hold relevance
        to the severity of the age difference.

        Also returns true if the differnce is greater than 1,
        and false otherwise.
        """
        if segment == 0:
            diff = abs(age - 3)
        else:
            diff = age

        if diff >= 1:
            return diff, 1
        else:
            return diff, 0

    def extract_data(self, input_file):
        """Reads the input file and extracts data from it to assign to
        self.dataset. There are additional columns in self.dataset with
        values derived from input file attributes, for example, the age
        difference.

        Note that the input file does have an expected format, and
        will likely cause an error if the the input file is not in the
        correct format.

        The input file is made by copying the tables on page 5 and 6 of
        the Capsim fasttrack report, then adding the segment and round
        columns on the end.

        This function uses the private helper functions above.

        Important Note: This function will delete and overwrite any 
        previous dataset stored in this object.
        """
        self.dataset = np.empty((0, 25))

        with open(input_file, "r") as input_f:
            lines = input_f.readlines()

        for i in lines:
            if i[0] != "#" and i[0] != "\n":
                orig_attri = i.strip().split(" ")

                # If the element at index 4 isn't 'YES', then insert 'NO'
                # into index 4, so attribute indexes match. Reason this is
                # necessary is because when I copied and pasted the table
                # from the fasttrack, if a product stocked out, then in
                # that column, the value will be 'YES'. But if the product
                # didn't stock out, then the column will be blank, causing
                # products that didn't stock out have 16 attributes
                # (including manually added 2 at the end), and products
                # that did stock out to have 17 attributes.
                if orig_attri[4] != "YES":
                    orig_attri.insert(4, "NO")

                row = np.array(
                    [
                        # Name (idx 0)
                        orig_attri[0],
                        # Market Share (idx 1)
                        float(orig_attri[1].strip("%")) / 100,
                        # Units Sold (idx 2)
                        int(orig_attri[2].replace(",", "")),
                        # Revision Date (idx 3)
                        orig_attri[3],
                        # Stock Out (idx 4)
                        None,
                        # Pfmn (idx 5)
                        float(orig_attri[5]),
                        # Size (idx 6)
                        float(orig_attri[6]),
                        # Position Difference (idx 7)
                        None,
                        # Price (idx 8)
                        None,
                        # Price Difference (idx 9)
                        None,
                        # MTBF (idx 10)
                        int(orig_attri[8]),
                        # MTBF Score (idx 11)
                        None,
                        # Age (idx 12)
                        float(orig_attri[9]),
                        # Age Difference (idx 13)
                        None,
                        # Promo Budget (idx 14)
                        None,
                        # Cust. Aware (idx 15)
                        float(orig_attri[11].strip("%")) / 100,
                        # Sales Budget (idx 16)
                        None,
                        # Cust. Access (idx 17)
                        float(orig_attri[13].strip("%")) / 100,
                        # Segment (idx 18)
                        None,
                        # Current Round (idx 19)
                        int(orig_attri[16]),
                        # Position out of range (idx 20)
                        None,
                        # Price out of ideal range (idx 21)
                        None,
                        # MTBF out of ideal range (idx 22)
                        None,
                        # Age out of idea range (idx 23)
                        None,
                        # CSS (idx 24)
                        float(orig_attri[14]),
                    ]
                )

                # Change Stock Out to 1 for YES, 0 for NO (Keras needs
                # numeric input values).
                if orig_attri[4] == "YES":
                    row[4] = 1
                else:
                    row[4] = 0

                # Price
                row[8] = float(orig_attri[7].replace("$", "").replace(",", ""))

                # Promo Budget
                row[14] = float(orig_attri[10].replace("$", "").replace(",", ""))

                # Sales Budget
                row[16] = float(orig_attri[12].replace("$", "").replace(",", ""))

                # Change Segment from LOW and HIGH to 0 and 1
                # respectively (Keras needs numeric input values).
                if orig_attri[15] == "LOW":
                    row[18] = 0
                else:
                    row[18] = 1

                # Position Difference and position out of range
                row[7], row[20] = self._get_position_diff(
                    row[5], row[6], row[19], row[18]
                )

                # Price Difference and price out of range
                row[9], row[21] = self._get_price_score(row[8], row[18])

                # MTBF Score and mtbf out of range
                row[11], row[22] = self._get_MTBF_score(row[10], row[18])

                # Age Difference and age out of range
                row[13], row[23] = self._get_age_diff(row[12], row[18])

                # Add row to self.dataset
                self.dataset = np.vstack((self.dataset, row))

    def write_to_csv(self, file_name="./dataset.csv"):
        """Writes the dataset (including attribute names) to an output
        csv file.

        Note: The output file will be overwritten.
        """
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            # Write headers first
            writer.writerow(self.get_headers())

            # Write dataset
            writer.writerows(self.dataset)

    def get_dataset(self, with_headers=True):
        """Returns a copy of the dataset"""
        copy = np.copy(self.dataset)
        if with_headers:
            return copy
        else:
            # Returns dataset without first row which is the headers
            return np.delete(copy, 0, axis=0)


if __name__ == "__main__":
    # Test case for extracting data and saving to csv file
    test = ExtractData()
    test.extract_data("./input_file.txt")
    test.write_to_csv()

    test.load_dataset("./dataset.csv")
    test.write_to_csv()
    print(test.get_dataset(with_headers=False))
