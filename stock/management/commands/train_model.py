from django.core.management.base import BaseCommand
from stock.dataframe_nepse import stock_dataFrame
from stock.helper import prepare_data, train_and_test
from datetime import datetime  # Import datetime module

class Command(BaseCommand):
    help = 'Retrains the stock forecasting model'

    def handle(self, *args, **kwargs):
        self.stdout.write("Retraining model...")
        symbol = 'UNL'
        df = stock_dataFrame(symbol)
        df, model_path = prepare_data(df, symbol)
        mape, test_mape, predicted_tomorrow_price_original = train_and_test(df, model_path)

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write test_mape and timestamp to a text file
        with open("training_log.txt", "a") as file:  # Use "a" to append to the file
            file.write(f"{current_time} - Test MAPE: {test_mape}\n")

        self.stdout.write(self.style.SUCCESS("Model retraining completed. Results logged in training_log.txt."))