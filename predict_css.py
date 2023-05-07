"""
By: Andrew Hunter
Date: May 7, 2023

This file builds a neural network to predict the CSS of a product. 
More precisely, 2 models are built, one to predict the CSS in the low 
tech segment, and a different model for the high tech segment.
"""

import numpy as np
import tensorflow as tf
import csv
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, load_model

from extract_data import ExtractData


class PredictCSS:
    def __init__(self, dataset):
        """Initalizes hyperparameters and other class-wide variables"""
        self.dataset = dataset
        
        self.low_data = None
        self.high_data = None

        #self.model = None
        self.low_model = None
        self.high_model = None

        # Hyperparameters
        self.test_size = 0.2
        self.loss_func = "mean_squared_error"
        self.batch_size = 2
        self.epochs = 1500
        self.learning_rate = 0.3
        self.l1 = 0.1
        self.l2 = 0.1

    def load_model(self, low_model, high_model):
        """Loads previously saved low and high model"""
        self.low_model = load_model(low_model)
        self.high_model = load_model(high_model)

    def build(self):
        """Builds the 2 models, including processing the data, 
        splitting the data, and testing the model.
		"""
        self.preprocess()

        # Clear contents of test_results file and write headers
        with open("./test_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Segment", "Actual CSS", "Predicted CSS"])

        # Build low model
        self.low_model, low_loss, low_mae = self._build_model(self.low_data)
        self.save_model(self.low_model, "low model")
        print("low model built and saved")

        # Build high model
        self.high_model, high_loss, high_mae = self._build_model(self.high_data)
        self.save_model(self.high_model, "high model")
        print("high model built and saved")

        # Print statistics
        print("low model loss: ", low_loss, "low model mae: " , low_mae)
        print("high model loss: ", high_loss, "high model mae: " , high_mae)

    def preprocess(self):
        """Applies modifications to the data in an attempt to help the 
        model train. For example, since we're building 2 separate 
        models for the low and high tech segments, there's no reason 
        to have a segment attribute, since all tuples will have the 
        same value.

		Other attributes that can't be used in the prediciton of the 
        CSS are also excluded. For exmample, the market share is 
        dependent on the CSS, not the other way around. Since a user 
        wouldn't know the market share when they're predicting the CSS, 
        it's not fair to include this attribute in the model.
		
        Note: Since the dataset is so small, I'm not worried about 
        efficiency.
        """
        # Remove all products that are stocked out. This is a design 
        # decision I made to improve the accuracy of the model, 
        # sacrificing the ability for users to precict their CSS if it 
        # sells out, 1 of the 2 main reasons for predicting the CSS is 
        # to have enough inventory to not stock out. I don't see any 
        # reason a user would want to predict a product's CSS with the 
        # assumption of it stocking out.
        rows_to_delete = []
        for i in range(self.dataset.shape[0]):
            if self.dataset[i, 4] == 1:
                rows_to_delete.append(i)
        self.dataset = np.delete(self.dataset, rows_to_delete, axis=0)

        # Remove following columns: Name, Market Share, Units Sold,
        # Revision Date, and stock out.
        self.dataset = np.delete(self.dataset, [0, 1, 2, 3, 4], axis=1)

        # Convert dataset to types compatible with tensorflow
        self.dataset = np.asarray(self.dataset).astype(np.float32)

        # split dataset into high and low by segment
        low = np.empty((0, self.dataset.shape[1]))
        high = np.empty((0, self.dataset.shape[1]))
        for i in self.dataset:
            # If segment (new idx for segment is 13) is 0, then put into low
            if i[13] == 0:
                low = np.vstack((low, i))
            else:
                high = np.vstack((high, i))

        # self.low_data will have form `(x_train, x_test, css_train, css_test)`
        self.low_data = train_test_split(
            low[:, :-1], low[:, -1], test_size=self.test_size, shuffle=True)

        self.high_data = train_test_split(
            high[:, :-1], high[:, -1], test_size=self.test_size, shuffle=True) 

    def _build_model(self, data):
        """Trains and tests a model. Returns the model.
        
        The input `data` has form (x_train, x_test, css_train, css_test)
        """
        x_train = data[0]
        x_test = data[1]
        css_train = data[2]
        css_test = data[3]

        # Configure optimizer
        tf.keras.optimizers.Adam(learning_rate=self.learning_rate)

        # Configure Regularization
        tf.keras.regularizers.L1L2(l1=self.l1, l2=self.l2)

        # Set up model architecture
        model = Sequential()
        model.add(
            Dense(units=32, activation="relu", input_dim=x_train[0].size)
        )
        model.add(Dense(units=64, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=16, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(units=1, activation="linear"))
        model.compile(loss=self.loss_func, optimizer="adam", metrics="mae")

        # Fit model
        model.fit(x_train, css_train, epochs=self.epochs, batch_size=self.batch_size)

        # Test Model
        loss, mae = self.test_model(model, x_test, css_test)

        return model, loss, mae

    def test_model(self, model, x_test, css_test):
        """Given a model and test data, returns the loss and mean 
        absolute error.
        """
        loss, mae = model.evaluate(x_test, css_test)

        with open("./test_results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            output = np.append(
                np.append(
                    x_test[:, 13].reshape(-1,1), css_test.reshape(-1,1), axis=1
                ), model.predict(x_test), axis=1
            )
            writer.writerows(output)

        print("loss: ", loss, "mae: ", mae)
        return loss, mae

    def save_model(self, model, name="most_recent_model"):
        """Saves the inputted model in the path: `name` to be reloaded at a later time.
        """
        model.save(name)


if __name__ == "__main__":
    data = ExtractData()
    data.load_dataset("./dataset.csv")
    test_model = PredictCSS(data.get_dataset(with_headers=False))
    test_model.build()
