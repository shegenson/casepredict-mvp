import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as pd_stream
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CasePredict AI | Legal Decision Support",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR PROFESSIONAL LAWYER UI ---
st.markdown(
    """
    <style>
    .reportview-container { background: #f5f7f8; }
    .main .block-container { padding-top: 2rem; }
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #172554;
        border-color: #172554;
    }
    .disclaimer-box {
        background-color: #FEF2F2;
        border-left: 4px solid #DC2626;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 2rem;
    }
    .disclaimer-text { color: #991B1B; font-size: 0.9rem; font-weight: 500; }
    .source-label { color: #6B7280; font-size: 0.8rem; font-style: italic; }
    </style>
""",
    unsafe_allow_html=True,
)


# --- MOCK DATA ENGINE (20 Fake Precedents) ---
@st.cache_data
def get_mock_case_db():
    return [
        {
            "facts": "Breach of contract regarding software delivery delays and IP ownership.",
            "outcome": "Win",
            "judge": "Hon. Justice Ademola",
            "citation": "(2024) FHC/L/CS/402",
            "excerpt": "...where time is of the essence in a technology service agreement, unexcused delay constitutes a material breach allowing rescission.",
            "type": "Civil",
        },
        {
            "facts": "Unlawful termination of employment without compliance with statutory notice period.",
            "outcome": "Settle",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2023) NICN/ABJ/12",
            "excerpt": "Employment contracts governed by statute must strictly adhere to procedural layout before termination is deemed valid.",
            "type": "Labor",
        },
        {
            "facts": "Corporate fraud and misappropriation of shareholder funds by director.",
            "outcome": "Lose",
            "judge": "Hon. Justice Aloma",
            "citation": "(2025) SC/CR/881",
            "excerpt": "The fiduciary duty of a director is absolute; however, criminal intent must be proven beyond reasonable doubt by the prosecution.",
            "type": "Criminal",
        },
        {
            "facts": "Intellectual property infringement over trademark look-alike in retail.",
            "outcome": "Win",
            "judge": "Hon. Justice Ademola",
            "citation": "(2023) FHC/IKJ/99",
            "excerpt": "The test for trademark infringement remains the likelihood of confusing an average consumer in the open marketplace.",
            "type": "Civil",
        },
        {
            "facts": "Claim for unpaid severance packages and accrued leave allowances post-merger.",
            "outcome": "Win",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2024) NICN/LA/405",
            "excerpt": "Surviving entities in a corporate merger inherit both the liabilities and outstanding labor obligations of the absorbed entity.",
            "type": "Labor",
        },
        {
            "facts": "Alleged tax evasion and falsification of customs import declarations.",
            "outcome": "Lose",
            "judge": "Hon. Justice Aloma",
            "citation": "(2022) CA/L/204X",
            "excerpt": "Discrepancies in revenue documentation do not automatically equate to fraud without proof of deliberate intent to deceive.",
            "type": "Criminal",
        },
        {
            "facts": "Property boundary dispute and trespass claims on commercial land.",
            "outcome": "Settle",
            "judge": "Hon. Justice Ademola",
            "citation": "(2021) HC/FL/55",
            "excerpt": "Long possession without challenge creates a heavy presumption of valid occupancy which requires definitive surveying proof to overturn.",
            "type": "Civil",
        },
        {
            "facts": "Enforcement of non-compete clause against executive moving to a direct competitor.",
            "outcome": "Lose",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2025) NICN/LA/11",
            "excerpt": "Covenants in restraint of trade are strictly construed and will be struck down if the geographical scope is unreasonably broad.",
            "type": "Labor",
        },
        {
            "facts": "Cyber-security breach and negligent handling of sensitive user data.",
            "outcome": "Win",
            "judge": "Hon. Justice Aloma",
            "citation": "(2024) FHC/ABJ/CR/72",
            "excerpt": "Failure to deploy industry-standard encryption protocols constitutes a prima facie case of operational negligence.",
            "type": "Civil",
        },
        {
            "facts": "Money laundering allegations tied to offshore shell companies.",
            "outcome": "Lose",
            "judge": "Hon. Justice Ademola",
            "citation": "(2023) FHC/L/512C",
            "excerpt": "The prosecution must establish a clear nexus between the illicit origin of funds and the financial accounts under review.",
            "type": "Criminal",
        },
        {
            "facts": "Constructive dismissal claim due to hostile work environment and harassment.",
            "outcome": "Win",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2024) NICN/ABJ/90",
            "excerpt": "Where an employer makes conditions intolerable, resignation is treated not as voluntary, but as a forced dismissal.",
            "type": "Labor",
        },
        {
            "facts": "Breach of a commercial lease agreement and failure to pay rent arrears.",
            "outcome": "Win",
            "judge": "Hon. Justice Aloma",
            "citation": "(2023) HC/OJO/30",
            "excerpt": "A lessor is legally entitled to re-entry upon persistent default of rent, subject to the service of proper statutory notices.",
            "type": "Civil",
        },
        {
            "facts": "Insider trading charges brought by SEC against a compliance officer.",
            "outcome": "Lose",
            "judge": "Hon. Justice Ademola",
            "citation": "(2025) SC/CR/104",
            "excerpt": "Possession of non-public information alone does not suffice; there must be proof of utilization or tipping for material gain.",
            "type": "Criminal",
        },
        {
            "facts": "Dispute over wrongful deduction of commissions for independent agents.",
            "outcome": "Settle",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2022) NICN/LA/112",
            "excerpt": "Ambiguities in commission structures drafted solely by the principal will be interpreted in favor of the agent.",
            "type": "Labor",
        },
        {
            "facts": "Product liability lawsuit involving contaminated pharmaceuticals.",
            "outcome": "Win",
            "judge": "Hon. Justice Aloma",
            "citation": "(2024) CA/B/89",
            "excerpt": "Manufacturers owe a duty of care to ultimate consumers that cannot be delegated or insulated by third-party distribution chains.",
            "type": "Civil",
        },
        {
            "facts": "Embezzlement of public funds via fraudulent procurement contracts.",
            "outcome": "Win",
            "judge": "Hon. Justice Ademola",
            "citation": "(2023) FHC/ABJ/311",
            "excerpt": "Inflated contracts and circumvention of the Public Procurement Act form a strong basis for criminal conversion of public wealth.",
            "type": "Criminal",
        },
        {
            "facts": "Unfair labor practice regarding unilateral reduction of employee benefits.",
            "outcome": "Win",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2023) NICN/KND/45",
            "excerpt": "Vested employment benefits form part of the fundamental terms of service and cannot be altered globally without mutual consent.",
            "type": "Labor",
        },
        {
            "facts": "Copyright infringement claim against an entertainment broadcasting network.",
            "outcome": "Settle",
            "judge": "Hon. Justice Aloma",
            "citation": "(2025) FHC/L/CS/77",
            "excerpt": "Substantial similarity in creative expression must be weighed against the doctrine of fair dealing and transformative public use.",
            "type": "Civil",
        },
        {
            "facts": "Armed robbery and conspiracy charges in a residential zone.",
            "outcome": "Lose",
            "judge": "Hon. Justice Ademola",
            "citation": "(2022) HC/IKJ/CR/04",
            "excerpt": "Identification evidence must be clear, unequivocal, and free from external suggestion to sustain a conviction for capital offences.",
            "type": "Criminal",
        },
        {
            "facts": "Workplace injury due to lack of adequate personal protective equipment (PPE).",
            "outcome": "Win",
            "judge": "Hon. Justice Awotoye",
            "citation": "(2024) NICN/PH/18",
            "excerpt": "Statutory duties under the Factories Act impose strict liability on employers to guarantee a safe theater of operation.",
            "type": "Labor",
        },
    ]


# --- RISK & COUNTER-ARGUMENT GENERATORS ---
def generate_insights(case_type):
    risks_map = {
        "Civil": [
            "Statute of limitations limitations on old evidence",
            "Ambiguity in contract Clause 14 (Indemnity Exception)",
            "High evidentiary burden for proving non-liquidated damages",
        ],
        "Criminal": [
            "Heavy reliance on circumstantial eyewitness testimonies",
            "Potential gaps in continuous chain of custody for digital forensics",
            "Strict interpretation of criminal intent (Mens Rea)",
        ],
        "Labor": [
            "Inconsistent historical disciplinary tracking by HR",
            "Verbal assurances made by line managers conflicting with written policies",
            "Strict pro-employee tendencies in modern statutory interpretations",
        ],
    }
    counters_map = {
        "Civil": [
            "Opposing counsel will claim waiver of rights by conduct over time.",
            "Defense will argue force majeure due to macroeconomic shocks.",
        ],
        "Criminal": [
            "Prosecution will present alternative theories of joint enterprise.",
            "The state will argue standard operating procedures were fully met.",
        ],
        "Labor": [
            "Claimant will assert constructive dismissal based on mitigation failure.",
            "Opposing side will argue failure to exhaust internal grievance mechanisms.",
        ],
    }
    return risks_map.get(case_type, risks_map["Civil"]), counters_map.get(
        case_type, counters_map["Civil"]
    )


# --- APPLICATION LAYOUT ---
st.title("⚖️ CasePredict AI")
st.subheader("Predictive Analytics & Decision Support for Legal Professionals")

# 1. Disclaimer Banner
st.markdown(
    """
    <div class="disclaimer-box">
        <span class="disclaimer-text">
            ⚠️ <strong>DISCLAIMER:</strong> This platform is a decision support tool powered by predictive modeling and mock legal records. It does not constitute formal legal advice, structural counsel, or a binding guarantee of judicial outcomes.
        </span>
    </div>
""",
    unsafe_allow_html=True,
)

# Main Form Split Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 🔍 Case Parameters")
    with st.form("case_input_form"):
        case_facts = st.text_area(
            "Case Facts / Synopsis",
            placeholder="Type or paste the core facts of the brief here...",
            height=150,
        )

        jurisdiction = st.selectbox(
            "Jurisdiction / Forum",
            [
                "Magistrate Court",
                "High Court",
                "Federal High Court",
                "Court of Appeal",
                "Supreme Court",
            ],
        )

        case_type = st.selectbox("Case Classification", ["Civil", "Criminal", "Labor"])

        judge_name = st.selectbox(
            "Presiding Jurist (Context)",
            [
                "Hon. Justice Ademola",
                "Hon. Justice Awotoye",
                "Hon. Justice Aloma",
                "Other / Unassigned",
            ],
        )

        submit_btn = st.form_submit_button("Predict Outcome")

# --- ENGINE LOGIC & VISUALIZATION ---
if submit_btn:
    if not case_facts.strip():
        st.warning("Please input case facts to run the predictive analysis.")
    else:
        # Business rules for deterministic mock predictions based on inputs
        if "breach" in case_facts.lower() or "termination" in case_facts.lower():
            win, lose, settle = 68, 12, 20
        elif "fraud" in case_facts.lower() or "evasion" in case_facts.lower():
            win, lose, settle = 35, 50, 15
        else:
            # Semi-random but clean distribution
            win = random.choice([55, 60, 45])
            settle = random.choice([20, 25, 15])
            lose = 100 - (win + settle)

        with col2:
            st.markdown("### 📊 Predictive Analysis Results")

            # Plotly Donut Chart
            labels = ["Win Probability", "Loss Probability", "Settlement Likelihood"]
            values = [win, lose, settle]
            colors = ["#1E3A8A", "#DC2626", "#F59E0B"]

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.5,
                        marker=dict(colors=colors),
                        textinfo="percent+label",
                    )
                ]
            )
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=260,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Risk Assessment & Arguments
            risks, counters = generate_insights(case_type)

            sub_c1, sub_c2 = st.columns(2)
            with sub_c1:
                st.markdown("#### ⚡ Top Risk Factors")
                for risk in risks:
                    st.markdown(f"- {risk}")

            with sub_c2:
                st.markdown("#### 🛡️ Anticipated Counter-Arguments")
                for counter in counters:
                    st.markdown(f"- *{counter}*")

        # --- SECTION 3: SHOW REASONING & PRECEDENTS ---
        st.markdown("---")
        st.markdown("### 📚 Judicial Reasoning & Precedent Mapping")

        # Filtering mock DB based on parameters for semantic realism
        db = get_mock_case_db()
        matching_cases = [c for c in db if c["type"] == case_type][:3]

        # Fallback if filters have zero length
        if len(matching_cases) < 3:
            matching_cases = db[:3]

        st.caption(
            "The following precedents share strategic clusters with your active factual scenario."
        )

        p_col1, p_col2, p_col3 = st.columns(3)
        cols = [p_col1, p_col2, p_col3]

        for idx, case in enumerate(matching_cases):
            with cols[idx]:
                st.info(f"**Precedent {idx+1}: {case['citation']}**")
                st.markdown(f"**Forum Jurist:** {case['judge']}")
                st.markdown(f"**Historical Target Outcome:** `{case['outcome']}`")
                st.markdown(f"> \"{case['excerpt']}\"")

        st.markdown(
            '<div class="source-label">Source: Court Records DB Ver 4.2.1 • Latency: 42ms</div>',
            unsafe_allow_html=True,
        )
else:
    with col2:
        st.info("Awaiting input parameters. Complete the form and select 'Predict Outcome' to generate actionable charts and analytical briefings.")
