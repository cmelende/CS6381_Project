import pandas as pd


class DataExplorationFrameFactory:

    @staticmethod
    def generate_notifier_dataframes(notifier_data_path: str) -> list[pd.DataFrame]:
        # notifier_1_sub_path = f"{notifier_data_path}/TEST-1SUB/all_data.csv"
        notifier_2_sub_path = f"{notifier_data_path}/TEST-2SUB/all_data.csv"
        notifier_4_sub_path = f"{notifier_data_path}/TEST-4SUB/all_data.csv"
        notifier_8_sub_path = f"{notifier_data_path}/TEST-8SUB/all_data.csv"
        notifier_16_sub_path = f"{notifier_data_path}/TEST-16SUB/all_data.csv"
        notifier_32_sub_path = f"{notifier_data_path}/TEST-32SUB/all_data.csv"
        notifier_64_sub_path = f"{notifier_data_path}/TEST-64SUB/all_data.csv"
        notifier_128_sub_path = f"{notifier_data_path}/TEST-128SUB/all_data.csv"
        notifier_256_sub_path = f"{notifier_data_path}/TEST-256SUB/all_data.csv"
        notifier_512_sub_path = f"{notifier_data_path}/TEST-512SUB/all_data.csv"
        notifier_2_sub_df = pd.read_csv(notifier_2_sub_path)
        notifier_4_sub_df = pd.read_csv(notifier_4_sub_path)
        notifier_8_sub_df = pd.read_csv(notifier_8_sub_path)
        notifier_16_sub_df = pd.read_csv(notifier_16_sub_path)
        notifier_32_sub_df = pd.read_csv(notifier_32_sub_path)
        notifier_64_sub_df = pd.read_csv(notifier_64_sub_path)
        notifier_128_sub_df = pd.read_csv(notifier_128_sub_path)
        notifier_256_sub_df = pd.read_csv(notifier_256_sub_path)
        notifier_512_sub_df = pd.read_csv(notifier_512_sub_path)
        notifier_data_frames: list[pd.DataFrame] = [
            notifier_2_sub_df,
            notifier_4_sub_df,
            notifier_8_sub_df,
            notifier_16_sub_df,
            notifier_32_sub_df,
            notifier_64_sub_df,
            notifier_128_sub_df,
            notifier_256_sub_df,
            notifier_512_sub_df
        ]

        return notifier_data_frames

    @staticmethod
    def generate_pub_sub_dataframes(pub_sub_data_path: str):
        # pub_sub_1_sub_path = f"{pub_sub_data_path}/TEST-1SUB/all_data.csv"
        pub_sub_2_sub_path = f"{pub_sub_data_path}/TEST-2SUB/all_data.csv"
        pub_sub_4_sub_path = f"{pub_sub_data_path}/TEST-4SUB/all_data.csv"
        pub_sub_8_sub_path = f"{pub_sub_data_path}/TEST-8SUB/all_data.csv"
        pub_sub_16_sub_path = f"{pub_sub_data_path}/TEST-16SUB/all_data.csv"
        pub_sub_32_sub_path = f"{pub_sub_data_path}/TEST-32SUB/all_data.csv"
        pub_sub_64_sub_path = f"{pub_sub_data_path}/TEST-64SUB/all_data.csv"
        pub_sub_128_sub_path = f"{pub_sub_data_path}/TEST-128SUB/all_data.csv"
        pub_sub_256_sub_path = f"{pub_sub_data_path}/TEST-256SUB/all_data.csv"
        pub_sub_512_sub_path = f"{pub_sub_data_path}/TEST-512SUB/all_data.csv"

        pub_sub_2_sub_df = pd.read_csv(pub_sub_2_sub_path)
        pub_sub_4_sub_df = pd.read_csv(pub_sub_4_sub_path)
        pub_sub_8_sub_df = pd.read_csv(pub_sub_8_sub_path)
        pub_sub_16_sub_df = pd.read_csv(pub_sub_16_sub_path)
        pub_sub_32_sub_df = pd.read_csv(pub_sub_32_sub_path)
        pub_sub_64_sub_df = pd.read_csv(pub_sub_64_sub_path)
        pub_sub_128_sub_df = pd.read_csv(pub_sub_128_sub_path)
        pub_sub_256_sub_df = pd.read_csv(pub_sub_256_sub_path)
        pub_sub_512_sub_df = pd.read_csv(pub_sub_512_sub_path)

        pub_sub_all_dfs: list[pd.DataFrame] = [
            pub_sub_2_sub_df,
            pub_sub_4_sub_df,
            pub_sub_8_sub_df,
            pub_sub_16_sub_df,
            pub_sub_32_sub_df,
            pub_sub_64_sub_df,
            pub_sub_128_sub_df,
            pub_sub_256_sub_df,
            pub_sub_512_sub_df
        ]

        return pub_sub_all_dfs
