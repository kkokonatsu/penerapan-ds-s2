import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import time
import random


st.set_page_config(page_title="Prediksi Status Mahasiswa", layout="wide")

marital_status_options = {
    'Single': 1, 'Married': 2, 'Widower': 3, 'Divorced': 4, 'Facto Union': 5, 'Legally Separated': 6
}
application_mode_options = {
    '1st phase - general contingent': 1, 'Ordinance No. 612/93': 2,
    '1st phase - special contingent (Azores Island)': 5, 'Holders of other higher courses': 7,
    'Ordinance No. 854-B/99': 10, 'International student (bachelor)': 15,
    '1st phase - special contingent (Madeira Island)': 16, '2nd phase - general contingent': 17,
    '3rd phase - general contingent': 18, 'Ordinance No. 533-A/99, item b2) (Different Plan)': 26,
    'Ordinance No. 533-A/99, item b3 (Other Institution)': 27, 'Over 23 years old': 39,
    'Transfer': 42, 'Change of course': 43, 'Technological specialization diploma holders': 44,
    'Change of institution/course': 51, 'Short cycle diploma holders': 53,
    'Change of institution/course (International)': 57
}
course_options = {
    'Biofuel Production Technologies': 33, 'Animation and Multimedia Design': 171,
    'Social Service (evening attendance)': 8014, 'Agronomy': 9003,
    'Communication Design': 9070, 'Veterinary Nursing': 9085,
    'Informatics Engineering': 9119, 'Equinculture': 9130,
    'Management': 9147, 'Social Service': 9238, 'Tourism': 9254,
    'Nursing': 9500, 'Oral Hygiene': 9556,
    'Advertising and Marketing Management': 9670, 'Journalism and Communication': 9773,
    'Basic Education': 9853, 'Management (evening attendance)': 9991
}
attendance_options = {'Daytime': 1, 'Evening': 0}
gender_options = {'Male': 1, 'Female': 0}
binary_options = {'Yes': 1, 'No': 0}
previous_qualification_options = {
    'Secondary education': 1, 'Higher education - bachelor\'s degree': 2,
    'Higher education - degree': 3, 'Higher education - master\'s': 4,
    'Higher education - doctorate': 5, 'Frequency of higher education': 6,
    '12th year of schooling - not completed': 9, '11th year of schooling - not completed': 10,
    'Other - 11th year of schooling': 12, '10th year of schooling': 14,
    '10th year of schooling - not completed': 15,
    'Basic education 3rd cycle (9th/10th/11th year) or equiv.': 19,
    'Basic education 2nd cycle (6th/7th/8th year) or equiv.': 38,
    'Technological specialization course': 39, 'Higher education - degree (1st cycle)': 40,
    'Professional higher technical course': 42, 'Higher education - master (2nd cycle)': 43
}
nacionality_options = {
    'Portuguese': 1, 'German': 2, 'Spanish': 6, 'Italian': 11, 'Dutch': 13,
    'English': 14, 'Lithuanian': 17, 'Angolan': 21, 'Cape Verdean': 22,
    'Guinean': 24, 'Mozambican': 25, 'Santomean': 26, 'Turkish': 32,
    'Brazilian': 41, 'Romanian': 62, 'Moldova (Republic of)': 100,
    'Mexican': 101, 'Ukrainian': 103, 'Russian': 105, 'Cuban': 108,
    'Colombian': 109
}
parent_qualification_options = {
    'Secondary Education - 12th Year of Schooling or Eq.': 1, 'Higher Education - Bachelor\'s Degree': 2,
    'Higher Education - Degree': 3, 'Higher Education - Master\'s': 4, 'Higher Education - Doctorate': 5,
    'Frequency of Higher Education': 6, '12th Year of Schooling - Not Completed': 9,
    '11th Year of Schooling - Not Completed': 10, '7th Year (Old)': 11,
    'Other - 11th Year of Schooling': 12, '10th Year of Schooling': 14,
    'General commerce course': 18, 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.': 19,
    'Technical-professional course': 22, '7th year of schooling': 26,
    '2nd cycle of the general high school course': 27, '9th Year of Schooling - Not Completed': 29,
    '8th year of schooling': 30, 'Unknown': 34, 'Can\'t read or write': 35,
    'Can read without having a 4th year of schooling': 36,
    'Basic education 1st cycle (4th/5th year) or equiv.': 37,
    'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.': 38,
    'Technological specialization course': 39, 'Higher education - degree (1st cycle)': 40,
    'Specialized higher studies course': 41, 'Professional higher technical course': 42,
    'Higher Education - Master (2nd cycle)': 43, 'Higher Education - Doctorate (3rd cycle)': 44
}
parent_occupation_options = {
    'Student': 0, 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers': 1,
    'Specialists in Intellectual and Scientific Activities': 2, 'Intermediate Level Technicians and Professions': 3,
    'Administrative staff': 4, 'Personal Services, Security and Safety Workers and Sellers': 5,
    'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry': 6, 'Skilled Workers in Industry, Construction and Craftsmen': 7,
    'Installation and Machine Operators and Assembly Workers': 8, 'Unskilled Workers': 9,
    'Armed Forces Professions': 10, 'Other Situation': 90, '(blank)': 99
}

higher_edu_codes = {2, 3, 4, 5, 6, 39, 40, 41, 42, 43, 44}
secondary_edu_codes = {1, 9, 10, 14, 15, 13, 18, 20, 25, 31, 33}
basic_edu_codes = {11, 19, 26, 27, 29, 30, 37, 38}
incomplete_other_codes = {12, 22, 34, 35, 36}
professional_managerial_codes = {1, 2, 112, 114, 121, 122, 123, 124, 125}
technical_associate_codes = {3, 131, 132, 134, 135}
administrative_clerical_codes = {4, 141, 143, 144}
service_sales_codes = {5, 151, 152, 153, 154, 195}
skilled_trades_codes = {7, 8, 171, 172, 173, 174, 175, 181, 182, 183}
agricultural_fishery_codes = {6, 161, 163, 192}
unskilled_elementary_codes = {9, 191, 193, 194}
specific_public_roles_codes = {10, 101, 102, 103}
student_codes = {0}
other_unknown_occ_codes = {90, 99}

# Reverse mapping untuk mengisi form dari data CSV
def get_key_from_value(d, value):
    """Mencari key di dictionary berdasarkan value-nya."""
    return next((k for k, v in d.items() if v == value), None)

@st.cache_resource 
def load_assets():
    models_dir = 'models'
    
    if not os.path.exists(models_dir):
        st.error(f"Folder '{models_dir}' tidak ditemukan. Pastikan ada dan berisi semua file yang diperlukan.")
        st.stop() 

    all_files_in_models = os.listdir(models_dir)

    label_encoders = {}
    scaler = None
    one_hot_encoder = None
    binary_encoder = None
    model = None
    final_feature_names = []

    # Memuat LabelEncoders
    for filename in all_files_in_models:
        if filename.startswith('label_encoder_') and filename.endswith('.joblib'):
            col_name = filename.replace('label_encoder_', '').replace('.joblib', '')
            file_path = os.path.join(models_dir, filename)
            try:
                label_encoders[col_name] = joblib.load(file_path)
            except Exception as e:
                st.error(f"Gagal memuat LabelEncoder untuk '{col_name}' dari '{filename}': {e}")
                # st.stop() 


    # Memuat StandardScaler
    scaler_path = os.path.join(models_dir, 'standard_scaler.joblib')
    if os.path.exists(scaler_path):
        try:
            scaler = joblib.load(scaler_path)
        except Exception as e:
            st.error(f"Gagal memuat StandardScaler: {e}")
            # st.stop()
    else:
        st.warning("File 'standard_scaler.joblib' tidak ditemukan.")


    # Memuat OneHotEncoder
    ohe_path = os.path.join(models_dir, 'one_hot_encoder.joblib')
    if os.path.exists(ohe_path):
        try:
            one_hot_encoder = joblib.load(ohe_path)
        except Exception as e:
            st.error(f"Gagal memuat OneHotEncoder: {e}")
            # st.stop()
    else:
        st.warning("File 'one_hot_encoder.joblib' tidak ditemukan.")


    # Memuat BinaryEncoder
    be_path = os.path.join(models_dir, 'binary_encoder.joblib')
    if os.path.exists(be_path):
        try:
            binary_encoder = joblib.load(be_path)
        except Exception as e:
            st.error(f"Gagal memuat BinaryEncoder: {e}")
            # st.stop()
    else:
        st.warning("File 'binary_encoder.joblib' tidak ditemukan.")


    # Memuat Model XGBoost
    model_path = os.path.join(models_dir, 'xgboost_classifier_model.joblib')
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
        except Exception as e:
            st.error(f"Gagal memuat model klasifikasi (XGBoost): {e}. Pastikan folder 'models/' ada dan berisi semua file yang diperlukan.")
            st.stop() 
    else:
        st.error("File 'xgboost_classifier_model.joblib' tidak ditemukan. Aplikasi tidak dapat berjalan tanpa model.")
        st.stop()


    # Memuat final_feature_names
    feature_names_path = os.path.join(models_dir, 'final_feature_names.txt')
    if os.path.exists(feature_names_path):
        try:
            with open(feature_names_path, 'r') as f:
                final_feature_names = [line.strip() for line in f if line.strip()]
        except Exception as e:
            st.error(f"Gagal memuat nama fitur dari 'final_feature_names.txt': {e}")
            # st.stop()
    else:
        st.warning("File 'final_feature_names.txt' tidak ditemukan. Ini sangat disarankan untuk prediksi yang akurat.")
        # st.stop() 

    # st.success("Semua aset model berhasil dimuat.")
    return model, scaler, label_encoders, binary_encoder, one_hot_encoder, final_feature_names

def group_education_qualification_inference(qual_code):
    if qual_code in higher_edu_codes: return 'Higher Education'
    elif qual_code in secondary_edu_codes: return 'Secondary Education'
    elif qual_code in basic_edu_codes: return 'Basic Education'
    elif qual_code in incomplete_other_codes: return 'Incomplete/Other'
    else: return 'Unknown_Category'

def group_occupation_inference(occupation_code):
    if occupation_code in professional_managerial_codes: return 'Professional & Managerial'
    elif occupation_code in technical_associate_codes: return 'Technical & Associate Professionals'
    elif occupation_code in administrative_clerical_codes: return 'Administrative & Clerical'
    elif occupation_code in service_sales_codes: return 'Service & Sales Workers'
    elif occupation_code in skilled_trades_codes: return 'Skilled & Semi-Skilled Trades'
    elif occupation_code in agricultural_fishery_codes: return 'Agricultural & Fishery Workers'
    elif occupation_code in unskilled_elementary_codes: return 'Unskilled & Elementary Occupations'
    elif occupation_code in specific_public_roles_codes: return 'Specific Roles / Public Services'
    elif occupation_code in student_codes: return 'Student'
    elif occupation_code in other_unknown_occ_codes: return 'Other / Unknown'
    else: return 'Undefined Occupation'

def group_nacionality_inference(nacionality_code):
    return 'Portuguese' if nacionality_code == 1 else 'International'

def group_marital_status_inference(status_code):
    if status_code in [3, 4, 5, 6]: return 'Other_Status'
    elif status_code == 1: return 'Single'
    elif status_code == 2: return 'Married'
    else: return 'Unknown'
    
def preprocess_new_data(df_new, scaler, label_encoders, binary_encoder, one_hot_encoder, original_categorical_cols, original_numeric_cols):
    """
    Melakukan pra-pemrosesan pada data baru, mirip dengan pipeline pelatihan.
    Termasuk grouping, encoding, dan scaling.
    """
    df_processed = df_new.copy()
    
    # step 1: grouping
    grouping_map = {
        'Marital_status': group_marital_status_inference,
        'Previous_qualification': group_education_qualification_inference,
        'Mothers_qualification': group_education_qualification_inference,
        'Fathers_qualification': group_education_qualification_inference,
        'Mothers_occupation': group_occupation_inference,
        'Fathers_occupation': group_occupation_inference,
        'Nacionality': group_nacionality_inference,
    }
    for col, func in grouping_map.items():
        if col in df_processed.columns:
            df_processed[col] = df_processed[col].apply(func).astype('category')

    # step 2: feature engineering
    df_processed['Approval_Rate_1st_Sem'] = np.where(df_processed['Curricular_units_1st_sem_enrolled'] > 0,
                                                   df_processed['Curricular_units_1st_sem_approved'] / df_processed['Curricular_units_1st_sem_enrolled'], 0)
    df_processed['Approval_Rate_2nd_Sem'] = np.where(df_processed['Curricular_units_2nd_sem_enrolled'] > 0,
                                                   df_processed['Curricular_units_2nd_sem_approved'] / df_processed['Curricular_units_2nd_sem_enrolled'], 0)
    
    df_processed['No_Eval_Rate_1st_Sem'] = np.where(df_processed['Curricular_units_1st_sem_enrolled'] > 0,
                                                  df_processed['Curricular_units_1st_sem_without_evaluations'] / df_processed['Curricular_units_1st_sem_enrolled'], 0)
    df_processed['No_Eval_Rate_2nd_Sem'] = np.where(df_processed['Curricular_units_2nd_sem_enrolled'] > 0,
                                                  df_processed['Curricular_units_2nd_sem_without_evaluations'] / df_processed['Curricular_units_2nd_sem_enrolled'], 0)
    
    df_processed['Credit_Rate_1st_Sem'] = np.where(df_processed['Curricular_units_1st_sem_enrolled'] > 0,
                                                   df_processed['Curricular_units_1st_sem_credited'] / df_processed['Curricular_units_1st_sem_enrolled'], 0)
    df_processed['Credit_Rate_2nd_Sem'] = np.where(df_processed['Curricular_units_2nd_sem_enrolled'] > 0,
                                                   df_processed['Curricular_units_2nd_sem_credited'] / df_processed['Curricular_units_2nd_sem_enrolled'], 0)

    # Perubahan Kinerja Antar Semester (Delta Features)
    df_processed['Grade_Change_1st_2nd_Sem'] = df_processed['Curricular_units_2nd_sem_grade'] - df_processed['Curricular_units_1st_sem_grade']
    df_processed['Approval_Rate_Change_1st_2nd_Sem'] = df_processed['Approval_Rate_2nd_Sem'] - df_processed['Approval_Rate_1st_Sem']
    df_processed['Enrolled_Units_Change'] = df_processed['Curricular_units_2nd_sem_enrolled'] - df_processed['Curricular_units_1st_sem_enrolled']
    df_processed['No_Eval_Units_Change'] = df_processed['No_Eval_Rate_2nd_Sem'] - df_processed['No_Eval_Rate_1st_Sem']

    # Fitur Agregat / Kumulatif
    total_approved = df_processed['Curricular_units_1st_sem_approved'] + df_processed['Curricular_units_2nd_sem_approved']
    df_processed['Overall_Avg_Grade'] = np.where(total_approved > 0,
                                                 (df_processed['Curricular_units_1st_sem_grade'] * df_processed['Curricular_units_1st_sem_approved'] +
                                                  df_processed['Curricular_units_2nd_sem_grade'] * df_processed['Curricular_units_2nd_sem_approved']) / total_approved,
                                                 0)
    df_processed['Overall_Avg_Grade'] = np.where((total_approved == 0) & ((df_processed['Curricular_units_1st_sem_grade'] != 0) | (df_processed['Curricular_units_2nd_sem_grade'] != 0)),
                                                 (df_processed['Curricular_units_1st_sem_grade'] + df_processed['Curricular_units_2nd_sem_grade']) / 2,
                                                 df_processed['Overall_Avg_Grade'])
    
    df_processed['Total_Approved_Units'] = df_processed['Curricular_units_1st_sem_approved'] + df_processed['Curricular_units_2nd_sem_approved']
    df_processed['Total_Enrolled_Units'] = df_processed['Curricular_units_1st_sem_enrolled'] + df_processed['Curricular_units_2nd_sem_enrolled']
    df_processed['Total_No_Eval_Units'] = df_processed['Curricular_units_1st_sem_without_evaluations'] + df_processed['Curricular_units_2nd_sem_without_evaluations']

    # Perbedaan Nilai Masuk dan Kualifikasi Sebelumnya
    df_processed['Grade_Admission_PrevQual_Diff'] = df_processed['Admission_grade'] - df_processed['Previous_qualification_grade']
    
    # st.info("Melakukan dropping fitur yang tidak diperlukan...")
    columns_to_drop_inference = [
        'International',
        'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade', 'Approval_Rate_1st_Sem', 'Approval_Rate_2nd_Sem',
        'Curricular_units_1st_sem_credited', 'Curricular_units_2nd_sem_credited', 'Curricular_units_1st_sem_enrolled', 'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_1st_sem_evaluations', 'Curricular_units_2nd_sem_evaluations', 'Curricular_units_1st_sem_approved', 'Curricular_units_2nd_sem_approved',
        'Curricular_units_1st_sem_without_evaluations', 'Curricular_units_2nd_sem_without_evaluations', 'Credit_Rate_1st_Sem', 'No_Eval_Rate_1st_Sem', 'Total_No_Eval_Units',
        'Total_Enrolled_Units'
    ]
    
    # step 3: feature selection
    columns_to_drop_inference = [col for col in columns_to_drop_inference if col in df_processed.columns]
    df_processed = df_processed.drop(columns=columns_to_drop_inference, axis=1)
    # st.success(f"Fitur berhasil di-drop. Jumlah kolom saat ini: {df_processed.shape[1]}")

    # step 4: scalling & encoding
    # Fitur numerikal 
    numeric_features_to_scale = [
        'Application_order',
        'Previous_qualification_grade',
        'Admission_grade',
        'Age_at_enrollment',
        'Unemployment_rate',
        'Inflation_rate',
        'GDP',
        'No_Eval_Rate_2nd_Sem',
        'Credit_Rate_2nd_Sem',
        'Grade_Change_1st_2nd_Sem',
        'Approval_Rate_Change_1st_2nd_Sem',
        'Enrolled_Units_Change',
        'No_Eval_Units_Change',
        'Overall_Avg_Grade',
        'Total_Approved_Units',
        'Grade_Admission_PrevQual_Diff'
    ]

    # Fitur kategorikal yang akan di-Label Encode
    label_encode_features = [
        'Daytime_evening_attendance', 'Displaced', 'Educational_special_needs',
        'Debtor', 'Tuition_fees_up_to_date', 'Gender',
        'Scholarship_holder', 'Nacionality'
    ]

    # Fitur yang akan di-One-Hot Encode
    one_hot_features = [
        'Marital_status', 'Previous_qualification'
    ]

    # Fitur yang akan di-Binary Encode
    binary_encode_features = [
        'Application_mode', 'Course',
        'Mothers_qualification', 'Fathers_qualification',
        'Mothers_occupation', 'Fathers_occupation'
    ]

    df_encoded_temp = df_processed.copy()

    # Label Encoding
    # st.write("\n--- Melakukan Label Encoding pada data baru ---")
    # for col in label_encode_features: 
    #     if col in df_encoded_temp.columns and col in label_encoders: 
    #         try:
    #             df_encoded_temp[col] = label_encoders[col].transform(df_encoded_temp[col])
    #             # st.write(f"  - Kolom '{col}' berhasil di-Label Encode.")
    #         except Exception as e:
    #             st.warning(f"  - Gagal Label Encode kolom '{col}': {e}. Melewatkan kolom ini.")
     
    #     elif col not in df_encoded_temp.columns:
    #         st.warning(f"  - Kolom '{col}' (untuk Label Encode) tidak ditemukan di data input. Melewatkan.")
    #     else: 
    #         st.warning(f"  - LabelEncoder untuk kolom '{col}' tidak ditemukan dalam kamus encoder. Kolom ini tidak akan di-Label Encode.")


    # One-Hot Encoding
    # st.write("\n--- Melakukan One-Hot Encoding pada data baru ---")
    if one_hot_features and one_hot_encoder:
        cols_to_ohe = [col for col in one_hot_features if col in df_encoded_temp.columns]
        if cols_to_ohe:
            # Transform data using the loaded OneHotEncoder
            encoded_ohe_array = one_hot_encoder.transform(df_encoded_temp[cols_to_ohe])
            encoded_ohe_df = pd.DataFrame(encoded_ohe_array, columns=one_hot_encoder.get_feature_names_out(cols_to_ohe), index=df_encoded_temp.index)
            
            # Drop original columns and concatenate new ones
            df_encoded_temp = df_encoded_temp.drop(columns=cols_to_ohe)
            df_encoded_temp = pd.concat([df_encoded_temp, encoded_ohe_df], axis=1)
            # st.write(f"  - Fitur '{cols_to_ohe}' berhasil di-One-Hot Encode.")
        else:
            st.warning("  - Tidak ada kolom One-Hot Encoding yang ditemukan di data input.")
    else:
        st.warning("  - OneHotEncoder atau daftar 'one_hot_features' tidak valid. Melewatkan One-Hot Encoding.")

    # Binary Encoding
    # st.write("\n--- Melakukan Binary Encoding pada data baru ---")
    if binary_encode_features and binary_encoder:
        cols_to_be = [col for col in binary_encode_features if col in df_encoded_temp.columns]
        if cols_to_be:
            # BinaryEncoder mengembalikan DataFrame baru
            encoded_be_df = binary_encoder.transform(df_encoded_temp[cols_to_be])
            
            # Hapus kolom asli yang di-BE dan gabungkan yang baru
            df_encoded_temp = df_encoded_temp.drop(columns=cols_to_be)
            df_encoded_temp = pd.concat([df_encoded_temp, encoded_be_df], axis=1)
            # st.write(f"  - Fitur '{cols_to_be}' berhasil di-Binary Encode.")
        else:
            st.warning("  - Tidak ada kolom Binary Encoding yang ditemukan di data input.")
    else:
        st.warning("  - BinaryEncoder atau daftar 'binary_encode_features' tidak valid. Melewatkan Binary Encoding.")


    df_scaled_temp = df_encoded_temp.copy()
    
    cols_to_scale = [col for col in numeric_features_to_scale if col in df_scaled_temp.columns]

    if cols_to_scale and scaler:
        scaled_array = scaler.transform(df_scaled_temp[cols_to_scale])
        df_scaled_temp[cols_to_scale] = scaled_array
    elif not scaler:
        st.warning("Scaler tidak ditemukan. Fitur numerik tidak akan di-scale.")
    else:
        st.warning("Tidak ada kolom numerik yang ditemukan untuk di-scale.")

    return df_scaled_temp

# def apply_initial_mappings(df):
#     """
#     Menerapkan mapping awal dari nilai numerik ke label string untuk fitur kategorikal.
#     """
#     # NOTE: Dictionaries untuk mapping harus didefinisikan secara global
#     # agar bisa diakses di sini. Anda sudah melakukannya dengan benar.
#     df_mapped = df.copy()

#     # Menggunakan dictionary options yang sudah user-friendly
#     columns_to_map = {
#         'Marital_status': {v: k for k, v in marital_status_options.items()},
#         'Application_mode': {v: k for k, v in application_mode_options.items()},
#         'Course': {v: k for k, v in course_options.items()},
#         'Daytime_evening_attendance': {v: k for k, v in attendance_options.items()},
#         'Previous_qualification': {v: k for k, v in previous_qualification_options.items()},
#         'Nacionality': {v: k for k, v in nacionality_options.items()},
#         'Mothers_qualification': {v: k for k, v in parent_qualification_options.items()},
#         'Fathers_qualification': {v: k for k, v in parent_qualification_options.items()},
#         'Mothers_occupation': {v: k for k, v in parent_occupation_options.items()},
#         'Fathers_occupation': {v: k for k, v in parent_occupation_options.items()},
#         'Displaced': {v: k for k, v in binary_options.items()},
#         'Educational_special_needs': {v: k for k, v in binary_options.items()},
#         'Debtor': {v: k for k, v in binary_options.items()},
#         'Tuition_fees_up_to_date': {v: k for k, v in binary_options.items()},
#         'Gender': {v: k for k, v in gender_options.items()},
#         'Scholarship_holder': {v: k for k, v in binary_options.items()},
#         'International': {v: k for k, v in binary_options.items()},
#     }

#     for col_name, mapping_dict in columns_to_map.items():
#         if col_name in df_mapped.columns:
#             # Map dari angka ke string deskriptif
#             df_mapped[col_name] = df_mapped[col_name].map(mapping_dict).astype('category')
            
#     return df_mapped

def initialize_session_state():
    """Mengatur nilai default untuk semua field form di session state."""
    default_values = {
        # Demographics
        'Marital_status': 1, 'Nacionality': 1, 'Gender': 1, 'Age_at_enrollment': 18,
        # Application
        'Application_mode': 17, 'Application_order': 1, 'Course': 9119,
        'Daytime_evening_attendance': 1, 'Previous_qualification': 1,
        'Admission_grade': 120.0, 'Previous_qualification_grade': 120.0,
        # Socioeconomic & Support
        'Mothers_qualification': 1, 'Fathers_qualification': 1,
        'Mothers_occupation': 9, 'Fathers_occupation': 9,
        'Displaced': 0, 'Educational_special_needs': 0, 'Debtor': 0,
        'Tuition_fees_up_to_date': 1, 'Scholarship_holder': 0, 'International': 0,
        'Unemployment_rate': 12.0, 'Inflation_rate': 1.0, 'GDP': 0.0,
        # Academic - 1st Sem
        'Curricular_units_1st_sem_credited': 0, 'Curricular_units_1st_sem_enrolled': 6,
        'Curricular_units_1st_sem_evaluations': 6, 'Curricular_units_1st_sem_approved': 5,
        'Curricular_units_1st_sem_grade': 12.0, 'Curricular_units_1st_sem_without_evaluations': 0,
        # Academic - 2nd Sem
        'Curricular_units_2nd_sem_credited': 0, 'Curricular_units_2nd_sem_enrolled': 6,
        'Curricular_units_2nd_sem_evaluations': 6, 'Curricular_units_2nd_sem_approved': 5,
        'Curricular_units_2nd_sem_grade': 12.0, 'Curricular_units_2nd_sem_without_evaluations': 0,
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def display_prediction_form():
    with st.form(key='prediction_form'):
        st.subheader("Informasi Pribadi & Pendaftaran")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.Marital_status = marital_status_options[st.selectbox(
                "Status Pernikahan", options=list(marital_status_options.keys()),
                index=list(marital_status_options.values()).index(st.session_state.Marital_status)
            )]
            st.session_state.Application_mode = application_mode_options[st.selectbox(
                "Mode Pendaftaran", options=list(application_mode_options.keys()),
                index=list(application_mode_options.values()).index(st.session_state.Application_mode)
            )]
            st.session_state.Course = course_options[st.selectbox(
                "Program Studi", options=list(course_options.keys()),
                index=list(course_options.values()).index(st.session_state.Course)
            )]

        with c2:
            st.session_state.Gender = gender_options[st.selectbox(
                "Jenis Kelamin", options=list(gender_options.keys()),
                index=list(gender_options.values()).index(st.session_state.Gender)
            )]
            st.session_state.Application_order = st.number_input("Urutan Pilihan Pendaftaran", min_value=0, max_value=9, step=1, value=st.session_state.Application_order)
            st.session_state.Daytime_evening_attendance = attendance_options[st.selectbox(
                "Waktu Kuliah", options=list(attendance_options.keys()),
                index=list(attendance_options.values()).index(st.session_state.Daytime_evening_attendance)
            )]

        with c3:
            st.session_state.Age_at_enrollment = st.number_input("Usia Saat Mendaftar", min_value=17, max_value=70, value=st.session_state.Age_at_enrollment)
            st.session_state.Nacionality = nacionality_options[st.selectbox(
                "Kewarganegaraan", options=list(nacionality_options.keys()),
                index=list(nacionality_options.values()).index(st.session_state.Nacionality)
            )]
            st.session_state.International = binary_options[st.selectbox(
                "Mahasiswa Internasional?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.International)
            )]
        
        st.subheader("Informasi Latar Belakang & Keluarga")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.Previous_qualification = previous_qualification_options[st.selectbox(
                "Kualifikasi Sebelumnya", options=list(previous_qualification_options.keys()),
                index=list(previous_qualification_options.values()).index(st.session_state.Previous_qualification)
            )]
            st.session_state.Mothers_qualification = parent_qualification_options[st.selectbox(
                "Pendidikan Ibu", options=list(parent_qualification_options.keys()),
                index=list(parent_qualification_options.values()).index(st.session_state.Mothers_qualification)
            )]
            st.session_state.Mothers_occupation = parent_occupation_options[st.selectbox(
                "Pekerjaan Ibu", options=list(parent_occupation_options.keys()),
                index=list(parent_occupation_options.values()).index(st.session_state.Mothers_occupation)
            )]

        with c2:
            st.session_state.Previous_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya", min_value=0.0, max_value=200.0, value=st.session_state.Previous_qualification_grade)
            st.session_state.Fathers_qualification = parent_qualification_options[st.selectbox(
                "Pendidikan Ayah", options=list(parent_qualification_options.keys()),
                index=list(parent_qualification_options.values()).index(st.session_state.Fathers_qualification)
            )]
            st.session_state.Fathers_occupation = parent_occupation_options[st.selectbox(
                "Pekerjaan Ayah", options=list(parent_occupation_options.keys()),
                index=list(parent_occupation_options.values()).index(st.session_state.Fathers_occupation)
            )]

        st.subheader("Informasi Akademik & Keuangan")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.Scholarship_holder = binary_options[st.selectbox(
                "Penerima Beasiswa?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.Scholarship_holder)
            )]
            st.session_state.Tuition_fees_up_to_date = binary_options[st.selectbox(
                "Uang Kuliah Lunas?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.Tuition_fees_up_to_date)
            )]
            st.session_state.Debtor = binary_options[st.selectbox(
                "Memiliki Hutang?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.Debtor)
            )]

        with c2:
             st.session_state.Displaced = binary_options[st.selectbox(
                "Mahasiswa Pindahan?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.Displaced)
            )]
             st.session_state.Educational_special_needs = binary_options[st.selectbox(
                "Kebutuhan Khusus?", options=list(binary_options.keys()),
                index=list(binary_options.values()).index(st.session_state.Educational_special_needs)
            )]
             st.session_state.Admission_grade = st.number_input("Nilai Pendaftaran", min_value=0.0, max_value=200.0, value=st.session_state.Admission_grade)
        
        with c3:
            st.session_state.Unemployment_rate = st.number_input("Tingkat Pengangguran (%)", value=st.session_state.Unemployment_rate)
            st.session_state.Inflation_rate = st.number_input("Tingkat Inflasi (%)", value=st.session_state.Inflation_rate)
            st.session_state.GDP = st.number_input("GDP", value=st.session_state.GDP)

        st.subheader("Data Akademik Semester 1")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.Curricular_units_1st_sem_enrolled = st.number_input("SKS Diambil (Sem 1)", min_value=0, value=st.session_state.Curricular_units_1st_sem_enrolled)
            st.session_state.Curricular_units_1st_sem_credited = st.number_input("SKS Kredit (Sem 1)", min_value=0, value=st.session_state.Curricular_units_1st_sem_credited)
        with c2:
            st.session_state.Curricular_units_1st_sem_approved = st.number_input("SKS Lulus (Sem 1)", min_value=0, value=st.session_state.Curricular_units_1st_sem_approved)
            st.session_state.Curricular_units_1st_sem_evaluations = st.number_input("Jumlah Evaluasi (Sem 1)", min_value=0, value=st.session_state.Curricular_units_1st_sem_evaluations)
        with c3:
            st.session_state.Curricular_units_1st_sem_grade = st.number_input("Rata-rata Nilai (Sem 1)", min_value=0.0, max_value=20.0, value=st.session_state.Curricular_units_1st_sem_grade)
            st.session_state.Curricular_units_1st_sem_without_evaluations = st.number_input("SKS Tanpa Evaluasi (Sem 1)", min_value=0, value=st.session_state.Curricular_units_1st_sem_without_evaluations)
        
        st.subheader("Data Akademik Semester 2")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.Curricular_units_2nd_sem_enrolled = st.number_input("SKS Diambil (Sem 2)", min_value=0, value=st.session_state.Curricular_units_2nd_sem_enrolled)
            st.session_state.Curricular_units_2nd_sem_credited = st.number_input("SKS Kredit (Sem 2)", min_value=0, value=st.session_state.Curricular_units_2nd_sem_credited)
        with c2:
            st.session_state.Curricular_units_2nd_sem_approved = st.number_input("SKS Lulus (Sem 2)", min_value=0, value=st.session_state.Curricular_units_2nd_sem_approved)
            st.session_state.Curricular_units_2nd_sem_evaluations = st.number_input("Jumlah Evaluasi (Sem 2)", min_value=0, value=st.session_state.Curricular_units_2nd_sem_evaluations)
        with c3:
            st.session_state.Curricular_units_2nd_sem_grade = st.number_input("Rata-rata Nilai (Sem 2)", min_value=0.0, max_value=20.0, value=st.session_state.Curricular_units_2nd_sem_grade)
            st.session_state.Curricular_units_2nd_sem_without_evaluations = st.number_input("SKS Tanpa Evaluasi (Sem 2)", min_value=0, value=st.session_state.Curricular_units_2nd_sem_without_evaluations)
        
        submitted = st.form_submit_button("Prediksi Status Mahasiswa")
        return submitted


st.title("Sistem Prediksi Status Mahasiswa (Dropout/Non-Dropout)")

model, scaler, label_encoders, binary_encoder, one_hot_encoder, final_feature_names = load_assets()
target_mapping = {0: 'Non-Dropout', 1: 'Dropout'} 

initialize_session_state()

input_method = st.radio(
    "Pilih Metode Input Data:",
    ("Isi Form Secara Manual", "Unggah File CSV untuk Mengisi Form"),
    horizontal=True
)

if input_method == "Unggah File CSV untuk Mengisi Form":
    uploaded_file = st.file_uploader("Pilih file CSV", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File CSV berhasil diunggah. Form di bawah telah diisi dengan data dari baris pertama. Anda bisa mengubahnya sebelum prediksi.")
            
            data_row = df.iloc[0]

            for col_name in data_row.index:
                if col_name in st.session_state:
                    if isinstance(st.session_state[col_name], int):
                        st.session_state[col_name] = int(data_row[col_name])
                    elif isinstance(st.session_state[col_name], float):
                         st.session_state[col_name] = float(data_row[col_name])
                    else: 
                        st.session_state[col_name] = data_row[col_name]
        
        except Exception as e:
            st.error(f"Gagal memproses file CSV: {e}")

submitted = display_prediction_form()

if submitted:
    prediction_input_dict = {key: [st.session_state[key]] for key in st.session_state if key != 'input_method'}
    input_df = pd.DataFrame.from_dict(prediction_input_dict)

    st.write("Data yang akan dikirim untuk prediksi:")
    st.dataframe(input_df)

    with st.spinner("Melakukan pra-pemrosesan data dan prediksi..."):
        try:
            processed_data = preprocess_new_data(
                input_df, scaler, label_encoders, binary_encoder, 
                one_hot_encoder, ['daftar', 'kolom', 'kategorikal'], ['daftar', 'kolom', 'numerik']
            )
            # Sesuaikan dengan final features
            final_X = processed_data.reindex(columns=final_feature_names, fill_value=0)
            prediction_result = model.predict(final_X)
            prediction_proba = model.predict_proba(final_X)
            
            # test
            # time.sleep(2)
            # prediction_result = [random.choice([0, 1])]
            # prediction_proba = [[0.3, 0.7]] if prediction_result[0] == 1 else [[0.8, 0.2]]
            
            # show result
            final_prediction = "Dropout" if prediction_result[0] == 1 else "Non-Dropout"
            probability_dropout = prediction_proba[0][1]

            if final_prediction == "Dropout":
                st.error(f"**Prediksi Status: {final_prediction}**", icon="🚨")
            else:
                st.success(f"**Prediksi Status: {final_prediction}**", icon="✅")
            
            st.metric(label="Probabilitas Dropout", value=f"{probability_dropout:.2%}")
            st.progress(float(probability_dropout))


        except Exception as e:
            st.error("Terjadi kesalahan saat prediksi.")
            st.exception(e)