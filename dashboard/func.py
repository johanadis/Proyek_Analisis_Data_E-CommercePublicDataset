import base64


class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")[
            "product_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "product_id": "product_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(
            by='product_count', ascending=False)

        return sum_order_items_df

    def review_score_df(self):
        review_scores = self.df['review_score'].value_counts(
        ).sort_values(ascending=False)
        most_common_score = review_scores.idxmax()

        return review_scores, most_common_score

    def create_bystate_df(self):
        bystate_df = self.df.groupby(
            by="customer_state").customer_id.nunique().reset_index()
        bystate_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_common_state = bystate_df.loc[bystate_df['customer_count'].idxmax(
        ), 'customer_state']
        bystate_df = bystate_df.sort_values(
            by='customer_count', ascending=False)

        return bystate_df, most_common_state

    def create_order_status(self):
        order_status_df = self.df["order_status"].value_counts(
        ).sort_values(ascending=False)
        most_common_status = order_status_df.idxmax()

        return order_status_df, most_common_status


class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        brazil = self.mpimg.imread(self.urllib.request.urlopen(
            'https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(
            10, 10), alpha=0.3, s=0.3, c='green')
        self.plt.axis('off')
        self.plt.imshow(
            brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4])
        self.st.pyplot()


# Fungsi untuk mengonversi gambar menjadi Base64
def get_base64_image(image_path):
    """Mengonversi gambar menjadi format Base64 untuk digunakan dalam HTML."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
