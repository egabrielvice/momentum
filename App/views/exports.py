import streamlit as st

from database import *


def exports_page():
    st.header("Export / Backup")
    st.caption("Download your Momentum data as CSV files. This helps protect your logs before future upgrades.")

    tables = get_export_tables()

    for table_name, table_df in tables.items():
        st.subheader(table_name)

        if table_df.empty:
            st.info("No data yet.")
        else:
            st.dataframe(table_df, use_container_width=True)

            csv = table_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label=f"Download {table_name}.csv",
                data=csv,
                file_name=f"{table_name}.csv",
                mime="text/csv",
                key=f"download_{table_name}",
            )