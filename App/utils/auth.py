import streamlit as st


def require_password():
    """
    Private access gate.

    Local default password: momentum
    Deployment password: set APP_PASSWORD in Streamlit secrets.
    """
    try:
        expected_password = st.secrets.get("APP_PASSWORD", "momentum")
    except Exception:
        expected_password = "momentum"

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return

    # Align the Momentum label with the text inside the access card.
    st.markdown(
        """
        <div style="
            padding-left: 32px;
            margin-bottom: 12px;
            color: #9f1118;
            font-size: 14px;
            font-weight: 800;
            letter-spacing: 0.32em;
            text-transform: uppercase;
        ">
            MOMENTUM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-card">
            <h1>Private Access</h1>
            <p>Enter your password to open Momentum.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input("Password", type="password")

    if st.button("Enter Momentum"):
        if password == expected_password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()