'''

'''
import csv
import os
import traceback

from datetime import datetime

class EmailSchedule:
    def __init__(self):
        '''
        constructor to intialize below things
        self.products -> list of tuples , each tuple is the product 
                         ex- (customer_id, product_name, domain, start_date, duration)
        self.add_product_file -> csv file contains added product data in below format
                         ex - CustomerId,ProductName,Domain,StartDate,DurationMonths
        self.remove_product_file -> csv file contains remove product data in below format
                         ex - CustomerId,ProductName,Domain

        self.scheduled_email_data -> wrting scheduled email data into this csv file in below format
                         ex - CustomerID,ProductName,Domain,EmailDate
        '''
        self.products = []
        self.add_product_file = f"{os.path.dirname(os.path.realpath(__file__))}\\add_products.csv"
        self.remove_product_file = f"{os.path.dirname(os.path.realpath(__file__))}\\remove_products.csv"
        self.scheduled_email_data = f"{os.path.dirname(os.path.realpath(__file__))}\\scheduled_email_data.csv"

    @staticmethod
    def date_to_str(date):
        '''
        utility method to convert actual date object to string in the format %Y-%m-%d
        ex - 2021-03-27 to '2021-03-27'
        '''
        return datetime.strftime(date, '%Y-%m-%d')

    @staticmethod
    def str_to_date(string_date):
        '''
        utility method to convert actual string object to date in the format %Y-%m-%d
        ex - '2021-03-27' to 2021-03-27 
        '''
        return datetime.strptime(string_date, '%Y-%m-%d')

    def add_products(self):
        '''
        Read added products from csv file(self.add_product_file) 
        and add it to products data structure(self.products)
        '''
        with open(self.add_product_file) as f:
            csv_reader = csv.reader(f)
            next(csv_reader) #skip the header - CustomerId,ProductName,Domain,StartDate,DurationMonths
            for item in csv_reader:
                new_product = (item[0], item[1], item[2], self.str_to_date(item[3]), item[4])
                self.products.append(new_product)

        print(self.products)

    def remove_products(self):
        '''
        Read removed products from csv file(self.remove_product_file)
        and remove it from products data structure(self.products)
        '''
        with open(self.remove_product_file) as f:
            csv_reader = csv.reader(f)
            next(csv_reader) #skip the header - CustomerId,ProductName,Domain
            for item in csv_reader:
                remove_product = (item[0], item[1], item[2])
                for product in self.products:
                    if (product[0], product[1], product[2]) == remove_product:
                        self.products.remove(product)

        print(self.products)

    def scheduled_email(self):
        '''
        Detailed list of schedule mails data printing on console 
        and placing it in CSV file(self.scheduled_email_data)
        '''
        if self.products:
            #writing into csv file
            with open(self.scheduled_email_data, 'w') as f:
                #printing on console
                print("CustomerID ProductName Domain EmailDate")
                f.write("CustomerID,ProductName,Domain,EmailDate\n")

                for product in sorted(self.products, key=lambda x:x[3]):
                    convert_date_str = self.date_to_str(product[3])
                    print(product[0], product[1], product[2], convert_date_str)
                    f.write(f"{product[0]},{product[1]},{product[2]},{convert_date_str}\n")
        else:
            print("No products available for scheduling emails")

    def domain_send_mail(self):
        '''
        Domain sends email 2 days before expiration.
        '''
        pass

    def hosting_send_mail(self):
        '''
        Hosting sends email 1 day after activation and 3 days before expiration.
        '''
        pass

    def pdomain_send_mail(self):
        '''
        Protected Domain sends email 9 days before expiration and 2 days before expiration.
        '''
        pass

    def start_process(self):
        try:
            self.add_products()
            self.remove_products()
            self.scheduled_email()

            #sending mails , if require we can implement below methods
            self.domain_send_mail()
            self.hosting_send_mail()
            self.pdomain_send_mail()
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    s = EmailSchedule()
    s.start_process()