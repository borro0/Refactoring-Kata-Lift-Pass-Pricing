from lift_pass_pricing.db import create_lift_pass_db_connection


class PriceDataAccess:
    """Class which is used to access data required for price calculation"""

    def __init__(self, connection_options):
        self.connection = create_lift_pass_db_connection(connection_options)

    def store_pass_type_base_price(self, base_price, type):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) "
            + "ON DUPLICATE KEY UPDATE cost = ?",
            (type, base_price, base_price),
        )

    def get_pass_type_base_price(self, type):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT cost FROM base_price " + "WHERE type = ? ", (type,))
        row = cursor.fetchone()
        return row[0]

    def get_holidays(self):
        holidays = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM holidays")
        for row in cursor.fetchall():
            holidays.append(row[0])
        return holidays