import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

st.set_page_config(page_title="Prediksi Status Mahasiswa (Dropout/Non-Dropout)", layout="wide")

marital_status_mapping = {
    1: 'single', 2: 'married', 3: 'widower', 4: 'divorced', 5: 'facto union', 6: 'legally separated'
}
application_mode_mapping = {
    1: '1st phase - general contingent', 2: 'Ordinance No. 612/93',
    5: '1st phase - special contingent (Azores Island)', 7: 'Holders of other higher courses',
    10: 'Ordinance No. 854-B/99', 15: 'International student (bachelor)',
    16: '1st phase - special contingent (Madeira Island)', 17: '2nd phase - general contingent',
    18: '3rd phase - general contingent', 26: 'Ordinance No. 533-A/99, item b2) (Different Plan)',
    27: 'Ordinance No. 533-A/99, item b3 (Other Institution)', 39: 'Over 23 years old',
    42: 'Transfer', 43: 'Change of course', 44: 'Technological specialization diploma holders',
    51: 'Change of institution/course', 53: 'Short cycle diploma holders',
    57: 'Change of institution/course (International)'
}
course_mapping = {
    33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)', 9003: 'Agronomy',
    9070: 'Communication Design', 9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering', 9130: 'Equinculture',
    9147: 'Management', 9238: 'Social Service', 9254: 'Tourism',
    9500: 'Nursing', 9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management', 9773: 'Journalism and Communication',
    9853: 'Basic Education', 9991: 'Management (evening attendance)'
}
daytime_evening_attendance_mapping = {
    1: 'daytime', 0: 'evening'
}
previous_qualification_mapping = {
    1: 'Secondary education', 2: 'Higher education - bachelor\'s degree',
    3: 'Higher education - degree', 4: 'Higher education - master\'s',
    5: 'Higher education - doctorate', 6: 'Frequency of higher education',
    9: '12th year of schooling - not completed', 10: '11th year of schooling - not completed',
    12: 'Other - 11th year of schooling', 14: '10th year of schooling',
    15: '10th year of schooling - not completed',
    19: 'Basic education 3rd cycle (9th/10th/11th year) or equiv.',
    38: 'Basic education 2nd cycle (6th/7th/8th year) or equiv.',
    39: 'Technological specialization course', 40: 'Higher education - degree (1st cycle)',
    42: 'Professional higher technical course', 43: 'Higher education - master (2nd cycle)'
}
nacionality_mapping = {
    1: 'Portuguese', 2: 'German', 6: 'Spanish', 11: 'Italian', 13: 'Dutch',
    14: 'English', 17: 'Lithuanian', 21: 'Angolan', 22: 'Cape Verdean',
    24: 'Guinean', 25: 'Mozambican', 26: 'Santomean', 32: 'Turkish',
    41: 'Brazilian', 62: 'Romanian', 100: 'Moldova (Republic of)',
    101: 'Mexican', 103: 'Ukrainian', 105: 'Russian', 108: 'Cuban',
    109: 'Colombian'
}
mothers_qualification_mapping = {
    1: 'Secondary Education - 12th Year of Schooling or Eq.',
    2: 'Higher Education - Bachelor\'s Degree', 3: 'Higher Education - Degree',
    4: 'Higher Education - Master\'s', 5: 'Higher Education - Doctorate',
    6: 'Frequency of Higher Education', 9: '12th Year of Schooling - Not Completed',
    10: '11th Year of Schooling - Not Completed', 11: '7th Year (Old)',
    12: 'Other - 11th Year of Schooling', 14: '10th Year of Schooling',
    18: 'General commerce course',
    19: 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.',
    22: 'Technical-professional course', 26: '7th year of schooling',
    27: '2nd cycle of the general high school course',
    29: '9th Year of Schooling - Not Completed', 30: '8th year of schooling',
    34: 'Unknown', 35: 'Can\'t read or write',
    36: 'Can read without having a 4th year of schooling',
    37: 'Basic education 1st cycle (4th/5th year) or equiv.',
    38: 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.',
    39: 'Technological specialization course', 40: 'Higher education - degree (1st cycle)',
    41: 'Specialized higher studies course',
    42: 'Professional higher technical course', 43: 'Higher Education - Master (2nd cycle)',
    44: 'Higher Education - Doctorate (3rd cycle)'
}
fathers_qualification_mapping = {
    1: 'Secondary Education - 12th Year of Schooling or Eq.',
    2: 'Higher Education - Bachelor\'s Degree', 3: 'Higher Education - Degree',
    4: 'Higher Education - Master\'s', 5: 'Higher Education - Doctorate',
    6: 'Frequency of Higher Education', 9: '12th Year of Schooling - Not Completed',
    10: '11th Year of Schooling - Not Completed', 11: '7th Year (Old)',
    12: 'Other - 11th Year of Schooling', 13: '2nd year complementary high school course',
    14: '10th Year of Schooling', 18: 'General commerce course',
    19: 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.',
    20: 'Complementary High School Course', 22: 'Technical-professional course',
    25: 'Complementary High School Course - not concluded', 26: '7th year of schooling',
    27: '2nd cycle of the general high school course',
    29: '9th Year of Schooling - Not Completed', 30: '8th year of schooling',
    31: 'General Course of Administration and Commerce',
    33: 'Supplementary Accounting and Administration', 34: 'Unknown',
    35: 'Can\'t read or write',
    36: 'Can read without having a 4th year of schooling',
    37: 'Basic education 1st cycle (4th/5th year) or equiv.',
    38: 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.',
    39: 'Technological specialization course', 40: 'Higher education - degree (1st cycle)',
    41: 'Specialized higher studies course',
    42: 'Professional higher technical course', 43: 'Higher Education - Master (2nd cycle)',
    44: 'Higher Education - Doctorate (3rd cycle)'
}
mothers_occupation_mapping = {
    0: 'Student', 1: 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers',
    2: 'Specialists in Intellectual and Scientific Activities',
    3: 'Intermediate Level Technicians and Professions', 4: 'Administrative staff',
    5: 'Personal Services, Security and Safety Workers and Sellers',
    6: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry',
    7: 'Skilled Workers in Industry, Construction and Craftsmen',
    8: 'Installation and Machine Operators and Assembly Workers',
    9: 'Unskilled Workers', 10: 'Armed Forces Professions',
    90: 'Other Situation', 99: '(blank)', 122: 'Health professionals',
    123: 'teachers', 125: 'Specialists in information and communication technologies (ICT)',
    131: 'Intermediate level science and engineering technicians and professions',
    132: 'Technicians and professionals, of intermediate level of health',
    134: 'Intermediate level technicians from legal, social, sports, cultural and similar services',
    141: 'Office workers, secretaries in general and data processing operators',
    143: 'Data, accounting, statistical, financial services and registry-related operators',
    144: 'Other administrative support staff', 151: 'personal service workers',
    152: 'sellers', 153: 'Personal care workers and the like',
    171: 'Skilled construction workers and the like, except electricians',
    173: 'Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like',
    175: 'Workers in food processing, woodworking, clothing and other industries and crafts',
    191: 'cleaning workers',
    192: 'Unskilled workers in agriculture, animal production, fisheries and forestry',
    193: 'Unskilled workers in extractive industry, construction, manufacturing and transport',
    194: 'Meal preparation assistants'
}
fathers_occupation_mapping = {
    0: 'Student', 1: 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers',
    2: 'Specialists in Intellectual and Scientific Activities',
    3: 'Intermediate Level Technicians and Professions', 4: 'Administrative staff',
    5: 'Personal Services, Security and Safety Workers and Sellers',
    6: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry',
    7: 'Skilled Workers in Industry, Construction and Craftsmen',
    8: 'Installation and Machine Operators and Assembly Workers',
    9: 'Unskilled Workers', 10: 'Armed Forces Professions',
    90: 'Other Situation', 99: '(blank)', 101: 'Armed Forces Officers',
    102: 'Armed Forces Sergeants', 103: 'Other Armed Forces personnel',
    112: 'Directors of administrative and commercial services',
    114: 'Hotel, catering, trade and other services directors',
    121: 'Specialists in the physical sciences, mathematics, engineering and related techniques',
    122: 'Health professionals', 123: 'teachers',
    124: 'Specialists in finance, accounting, administrative organization, public and commercial relations',
    131: 'Intermediate level science and engineering technicians and professions',
    132: 'Technicians and professionals, of intermediate level of health',
    134: 'Intermediate level technicians from legal, social, sports, cultural and similar services',
    135: 'Information and communication technology technicians',
    141: 'Office workers, secretaries in general and data processing operators',
    143: 'Data, accounting, statistical, financial services and registry-related operators',
    144: 'Other administrative support staff', 151: 'personal service workers',
    152: 'sellers', 153: 'Personal care workers and the like',
    154: 'Protection and security services personnel',
    161: 'Market-oriented farmers and skilled agricultural and animal production workers',
    163: 'Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence',
    171: 'Skilled construction workers and the like, except electricians',
    172: 'Skilled workers in metallurgy, metalworking and similar',
    174: 'Skilled workers in electricity and electronics',
    175: 'Workers in food processing, woodworking, clothing and other industries and crafts',
    181: 'Fixed plant and machine operators', 182: 'assembly workers',
    183: 'Vehicle drivers and mobile equipment operators',
    192: 'Unskilled workers in agriculture, animal production, fisheries and forestry',
    193: 'Unskilled workers in extractive industry, construction, manufacturing and transport',
    194: 'Meal preparation assistants',
    195: 'Street vendors (except food) and street service providers'
}
binary_mapping = {1: 'yes', 0: 'no'}
gender_mapping = {1: 'male', 0: 'female'}
target_mapping = {0: 'Non-Dropout', 1: 'Dropout'} 

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

scaler, label_encoders, binary_encoder, one_hot_encoder, model, final_feature_names = load_assets()

def apply_initial_mappings(df):
    """
    Menerapkan mapping awal dari nilai numerik ke label string untuk fitur kategorikal.
    Ini harus cocok dengan langkah pertama pra-pemrosesan saat pelatihan.
    """
    df_mapped = df.copy()

    columns_to_map = {
        'Marital_status': marital_status_mapping,
        'Application_mode': application_mode_mapping,
        'Course': course_mapping,
        'Daytime_evening_attendance': daytime_evening_attendance_mapping,
        'Previous_qualification': previous_qualification_mapping,
        'Nacionality': nacionality_mapping,
        'Mothers_qualification': mothers_qualification_mapping,
        'Fathers_qualification': fathers_qualification_mapping,
        'Mothers_occupation': mothers_occupation_mapping,
        'Fathers_occupation': fathers_occupation_mapping,
        'Displaced': binary_mapping,
        'Educational_special_needs': binary_mapping,
        'Debtor': binary_mapping,
        'Tuition_fees_up_to_date': binary_mapping,
        'Gender': gender_mapping,
        'Scholarship_holder': binary_mapping,
        'International': binary_mapping,
    }

    # st.subheader("Debugging: apply_initial_mappings")

    for col_name, mapping_dict in columns_to_map.items():
        if col_name in df_mapped.columns:
            # st.write(f"\n--- Memproses Kolom: {col_name} ---")
            # st.write(f"Tipe data awal: {df_mapped[col_name].dtype}")
            # st.write(f"Nilai unik awal: {df_mapped[col_name].unique()}")

            # Pastikan kolom adalah tipe yang bisa di-map, seperti numerik atau object.
            # Jika sudah categorical dari input CSV, ini bisa jadi masalah.
            # Konversi ke object sementara untuk map/fillna yang aman.
            df_mapped[col_name] = df_mapped[col_name].astype(object) # Konversi ke object sementara

            # st.write(f"Tipe data setelah astype(object): {df_mapped[col_name].dtype}")

            mapped_series = df_mapped[col_name].map(mapping_dict)
            # st.write(f"Nilai unik setelah map(): {mapped_series.unique()}")
            # st.write(f"Jumlah NaN setelah map(): {mapped_series.isna().sum()}")


            all_possible_categories = list(mapping_dict.values())
            if 'Unknown' not in all_possible_categories: # Hindari duplikasi jika sudah ada di mapping
                all_possible_categories.append('Unknown')
            
            df_mapped[col_name] = mapped_series.fillna('Unknown')
            # st.write(f"Nilai unik setelah fillna('Unknown'): {df_mapped[col_name].unique()}")
            # st.write(f"Jumlah NaN setelah fillna('Unknown'): {df_mapped[col_name].isna().sum()}")

            try:
                df_mapped[col_name] = pd.Categorical(df_mapped[col_name], categories=all_possible_categories)
                # st.write(f"Sukses mengkonversi ke categorical dengan categories yang ditentukan.")
                # st.write(f"Kategori baru: {df_mapped[col_name].cat.categories.tolist()}")
                # st.write(f"Tipe data akhir untuk {col_name}: {df_mapped[col_name].dtype}")
            except Exception as e:
                st.error(f"ERROR saat mengkonversi '{col_name}' ke Categorical: {e}")
                st.error("Ini terjadi jika ada nilai yang tidak ada di `all_possible_categories`.")
                st.write(f"Nilai yang mencoba ditugaskan: {df_mapped[col_name].unique()}")
                st.stop() 

        else:
            st.warning(f"Kolom '{col_name}' tidak ditemukan di data input. Melewatkan mapping.")

    if 'Status' in df_mapped.columns:
        # st.write("\n--- Memproses Kolom: Status ---")
        # st.write(f"Tipe data awal Status: {df_mapped['Status'].dtype}")
        df_mapped['Status'] = df_mapped['Status'].astype('category')
        # st.write(f"Tipe data akhir Status: {df_mapped['Status'].dtype}")
        # st.write(f"Kategori Status: {df_mapped['Status'].cat.categories.tolist()}")


    return df_mapped

def preprocess_new_data(df_new, scaler, label_encoders, binary_encoder, one_hot_encoder, original_categorical_cols, original_numeric_cols):
    """
    Melakukan pra-pemrosesan pada data baru, mirip dengan pipeline pelatihan.
    Termasuk grouping, encoding, dan scaling.
    """
    df_processed = df_new.copy()
    
    st.info("Menerapkan mapping awal dari angka ke label kategori string...")
    df_processed = apply_initial_mappings(df_processed)
    st.success("Mapping awal selesai!")
    
    def group_education_qualification_inference(qual):
        higher_edu_quals = ['Higher education - degree', 'Higher education - degree (1st cycle)', 'Higher education - bachelor\'s degree', 'Higher education - master\'s', 'Higher education - master (2nd cycle)', 'Higher education - doctorate', 'Higher Education - Bachelor\'s Degree', 'Higher Education - Degree', 'Higher Education - Master\'s', 'Higher Education - Doctorate', 'Higher Education - Master (2nd cycle)', 'Higher Education - Doctorate (3rd cycle)', 'Frequency of Higher Education', 'Technological specialization course', 'Specialized higher studies course', 'Professional higher technical course']
        secondary_edu_quals = ['Secondary education', 'Secondary Education - 12th Year of Schooling or Eq.', '12th Year of Schooling - Not Completed', '11th Year of Schooling - Not Completed', '10th Year of Schooling', '10th Year of Schooling - Not Completed', '2nd year complementary high school course', 'General commerce course', 'Complementary High School Course', 'Complementary High School Course - not concluded', 'Supplementary Accounting and Administration']
        basic_edu_quals = ['Basic education 1st cycle (4th/5th year) or equiv.', 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equiv.', 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equiv.', '9th Year of Schooling - Not Completed', '8th year of schooling', '7th Year (Old)', '7th year of schooling', '2nd cycle of the general high school course']
        incomplete_other_quals = ['Unknown', 'Can\'t read or write', 'Can read without having a 4th year of schooling', 'Other - 11th Year of Schooling', 'Technical-professional course']
        
        if qual in higher_edu_quals: return 'Higher Education'
        elif qual in secondary_edu_quals: return 'Secondary Education'
        elif qual in basic_edu_quals: return 'Basic Education'
        elif qual in incomplete_other_quals: return 'Incomplete/Other'
        else: return 'Unknown_Category'

    def group_occupation_inference(occupation):
        professional_managerial = ['Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers', 'Specialists in Intellectual and Scientific Activities', 'Specialists in information and communication technologies (ICT)', 'Specialists in the physical sciences, mathematics, engineering and related techniques', 'Specialists in finance, accounting, administrative organization, public and commercial relations', 'Directors of administrative and commercial services', 'Hotel, catering, trade and other services directors']
        technical_associate = ['Intermediate Level Technicians and Professions', 'Intermediate level science and engineering technicians and professions', 'Technicians and professionals, of intermediate level of health', 'Intermediate level technicians from legal, social, sports, cultural and similar services', 'Information and communication technology technicians']
        administrative_clerical = ['Administrative staff', 'Office workers, secretaries in general and data processing operators', 'Data, accounting, statistical, financial services and registry-related operators', 'Other administrative support staff']
        service_sales = ['Personal Services, Security and Safety Workers and Sellers', 'personal service workers', 'sellers', 'Personal care workers and the like', 'Protection and security services personnel', 'Street vendors (except food) and street service providers']
        skilled_trades = ['Skilled Workers in Industry, Construction and Craftsmen', 'Skilled construction workers and the like, except electricians', 'Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like', 'Workers in food processing, woodworking, clothing and other industries and crafts', 'Skilled workers in metallurgy, metalworking and similar', 'Skilled workers in electricity and electronics', 'Fixed plant and machine operators', 'assembly workers', 'Vehicle drivers and mobile equipment operators']
        agricultural_fishery = ['Farmers and Skilled Workers in Agriculture, Fisheries and Forestry', 'Market-oriented farmers and skilled agricultural and animal production workers', 'Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence', 'Unskilled workers in agriculture, animal production, fisheries and forestry']
        unskilled_elementary = ['Unskilled Workers', 'Installation and Machine Operators and Assembly Workers', 'cleaning workers', 'Meal preparation assistants', 'Unskilled workers in extractive industry, construction, manufacturing and transport']
        specific_public_roles = ['Health professionals', 'teachers', 'Armed Forces Professions', 'Armed Forces Officers', 'Armed Forces Sergeants', 'Other Armed Forces personnel']
        student = ['Student']
        other_unknown_occ = ['Other Situation', '(blank)']

        if occupation in professional_managerial: return 'Professional & Managerial'
        elif occupation in technical_associate: return 'Technical & Associate Professionals'
        elif occupation in administrative_clerical: return 'Administrative & Clerical'
        elif occupation in service_sales: return 'Service & Sales Workers'
        elif occupation in skilled_trades: return 'Skilled & Semi-Skilled Trades'
        elif occupation in agricultural_fishery: return 'Agricultural & Fishery Workers'
        elif occupation in unskilled_elementary: return 'Unskilled & Elementary Occupations'
        elif occupation in specific_public_roles: return 'Specific Roles / Public Services'
        elif occupation in student: return 'Student'
        elif occupation in other_unknown_occ: return 'Other / Unknown'
        else: return 'Undefined Occupation'

    def group_nacionality_inference(nacionality):
        return 'Portuguese' if nacionality == 'Portuguese' else 'International'

    def group_marital_status_inference(status):
        if status in ['divorced', 'facto union', 'legally separated', 'widower']:
            return 'Other_Status'
        return status

    # Apply grouping functions
    if 'Marital_status' in df_processed.columns:
        df_processed['Marital_status'] = df_processed['Marital_status'].apply(group_marital_status_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Marital_status'])

    if 'Previous_qualification' in df_processed.columns:
        df_processed['Previous_qualification'] = df_processed['Previous_qualification'].apply(group_education_qualification_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Previous_qualification'])

    if 'Mothers_qualification' in df_processed.columns:
        df_processed['Mothers_qualification'] = df_processed['Mothers_qualification'].apply(group_education_qualification_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Mothers_qualification'])

    if 'Fathers_qualification' in df_processed.columns:
        df_processed['Fathers_qualification'] = df_processed['Fathers_qualification'].apply(group_education_qualification_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Fathers_qualification'])

    if 'Mothers_occupation' in df_processed.columns:
        df_processed['Mothers_occupation'] = df_processed['Mothers_occupation'].apply(group_occupation_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Mothers_occupation'])

    if 'Fathers_occupation' in df_processed.columns:
        df_processed['Fathers_occupation'] = df_processed['Fathers_occupation'].apply(group_occupation_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Fathers_occupation'])

    if 'Nacionality' in df_processed.columns:
        df_processed['Nacionality'] = df_processed['Nacionality'].apply(group_nacionality_inference).astype('category')
        # df_processed = df_processed.drop(columns=['Nacionality'])
    
    # Rasio Efisiensi Per Semester
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
    
    st.info("Melakukan dropping fitur yang tidak diperlukan...")
    columns_to_drop_inference = [
        'International',
        'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade', 'Approval_Rate_1st_Sem', 'Approval_Rate_2nd_Sem',
        'Curricular_units_1st_sem_credited', 'Curricular_units_2nd_sem_credited', 'Curricular_units_1st_sem_enrolled', 'Curricular_units_2nd_sem_enrolled',
        'Curricular_units_1st_sem_evaluations', 'Curricular_units_2nd_sem_evaluations', 'Curricular_units_1st_sem_approved', 'Curricular_units_2nd_sem_approved',
        'Curricular_units_1st_sem_without_evaluations', 'Curricular_units_2nd_sem_without_evaluations', 'Credit_Rate_1st_Sem', 'No_Eval_Rate_1st_Sem', 'Total_No_Eval_Units',
        'Total_Enrolled_Units'
    ]
    # Filter hanya kolom yang benar-benar ada di DataFrame sebelum drop
    columns_to_drop_inference = [col for col in columns_to_drop_inference if col in df_processed.columns]

    df_processed = df_processed.drop(columns=columns_to_drop_inference, axis=1)
    st.success(f"Fitur berhasil di-drop. Jumlah kolom saat ini: {df_processed.shape[1]}")

    # Fitur numerik yang akan discale
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
    for col in label_encode_features: # ITERASI HANYA PADA FITUR YANG HARUS DI-LABEL ENCODE
        if col in df_encoded_temp.columns and col in label_encoders: # Cek keberadaan kolom dan encoder
            try:
                df_encoded_temp[col] = df_encoded_temp[col].astype(str) # Pastikan tipe string untuk LE
                df_encoded_temp[col] = label_encoders[col].transform(df_encoded_temp[col])
                # st.write(f"  - Kolom '{col}' berhasil di-Label Encode.")
            except Exception as e:
                st.warning(f"  - Gagal Label Encode kolom '{col}': {e}. Melewatkan kolom ini.")
        elif col not in df_encoded_temp.columns:
            st.warning(f"  - Kolom '{col}' (untuk Label Encode) tidak ditemukan di data input. Melewatkan.")
        else: # Ini berarti kolom ada, tapi LabelEncoder-nya tidak dimuat/ditemukan.
            st.warning(f"  - LabelEncoder untuk kolom '{col}' tidak ditemukan dalam kamus encoder. Kolom ini tidak akan di-Label Encode.")


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

st.title("Sistem Prediksi Status Mahasiswa")
st.markdown("Unggah file CSV Anda untuk memprediksi apakah mahasiswa akan mengalami *dropout* atau tidak.")

model, scaler, label_encoders, binary_encoder, one_hot_encoder, final_feature_names = load_assets()

uploaded_file = st.file_uploader("Pilih file CSV", type="csv")

if uploaded_file is not None:
    st.info("File berhasil diunggah. Memulai pra-pemrosesan data...")
    try:
        input_df = pd.read_csv(uploaded_file)
        st.write("Preview Data Input:")
        st.dataframe(input_df.head())

        required_columns = [
            'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
            'Previous_qualification', 'Nacionality', 'Mothers_qualification', 'Fathers_qualification',
            'Mothers_occupation', 'Fathers_occupation', 'Displaced', 'Educational_special_needs',
            'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International',
            'Age_at_enrollment', 'Unemployment_rate', 'Inflation_rate', 'GDP',
            'Previous_qualification_grade', 'Admission_grade',
            'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled', 
            'Curricular_units_1st_sem_evaluations', 'Curricular_units_1st_sem_approved', 
            'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
            'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled', 
            'Curricular_units_2nd_sem_evaluations', 'Curricular_units_2nd_sem_approved', 
            'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations'
        ]

        missing_columns = [col for col in required_columns if col not in input_df.columns]

        if missing_columns:
            st.error(f"File CSV Anda tidak lengkap. Kolom berikut tidak ditemukan: **{', '.join(missing_columns)}**")
            st.warning("Pastikan file CSV Anda memiliki semua kolom yang diperlukan sesuai petunjuk.")
            st.stop()         
        st.success("Validasi format CSV berhasil. Semua kolom yang diperlukan ditemukan.")
        
        for col in ['Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
                    'Previous_qualification', 'Nacionality', 'Mothers_qualification', 'Fathers_qualification',
                    'Mothers_occupation', 'Fathers_occupation', 'Displaced', 'Educational_special_needs',
                    'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International']:
            if col in input_df.columns:
                input_df[col] = input_df[col].astype('category')

        original_numeric_cols = [
            'Age_at_enrollment', 'Unemployment_rate', 'Inflation_rate', 'GDP',
            'Previous_qualification_grade', 'Admission_grade',
            'Curricular_units_1st_sem_credited', 'Curricular_units_1st_sem_enrolled', 'Curricular_units_1st_sem_evaluations',
            'Curricular_units_1st_sem_approved', 'Curricular_units_1st_sem_grade', 'Curricular_units_1st_sem_without_evaluations',
            'Curricular_units_2nd_sem_credited', 'Curricular_units_2nd_sem_enrolled', 'Curricular_units_2nd_sem_evaluations',
            'Curricular_units_2nd_sem_approved', 'Curricular_units_2nd_sem_grade', 'Curricular_units_2nd_sem_without_evaluations'
        ]
        original_categorical_cols = [
            'Marital_status', 'Application_mode', 'Course', 'Daytime_evening_attendance',
            'Previous_qualification', 'Nacionality', 'Mothers_qualification', 'Fathers_qualification',
            'Mothers_occupation', 'Fathers_occupation', 'Displaced', 'Educational_special_needs',
            'Debtor', 'Tuition_fees_up_to_date', 'Gender', 'Scholarship_holder', 'International'
        ]


        st.info("Melakukan pra-pemrosesan pada data input...")
        processed_data_for_prediction = preprocess_new_data(
            input_df, scaler, label_encoders, binary_encoder, one_hot_encoder,
            original_categorical_cols, original_numeric_cols
        )
        st.success("Pra-pemrosesan selesai!")
        

        final_X = pd.DataFrame(columns=final_feature_names)
        
        for col in processed_data_for_prediction.columns:
            if col in final_X.columns:
                final_X[col] = processed_data_for_prediction[col]
        
        final_X = final_X.fillna(0) 

        # st.write("Preview Data Setelah Pra-pemrosesan dan Penyesuaian Kolom:")
        # st.dataframe(final_X.head())
        # st.write(f"Dimensi data yang akan diprediksi: {final_X.shape}")

        st.info("Melakukan prediksi...")
        predictions_numeric = model.predict(final_X)
        predictions_proba = model.predict_proba(final_X) 
        predictions_labels = pd.Series(predictions_numeric).map(target_mapping)

        input_df['Predicted_Status_Numeric'] = predictions_numeric
        input_df['Predicted_Status_Label'] = predictions_labels
        input_df['Probability_Non_Dropout'] = predictions_proba[:, 0]
        input_df['Probability_Dropout'] = predictions_proba[:, 1]
        
        st.success("Prediksi selesai!")
        st.write("Hasil Prediksi:")
        st.dataframe(input_df[['Predicted_Status_Label', 'Probability_Dropout']].head())
        
        st.download_button(
            label="Download Hasil Prediksi sebagai CSV",
            data=input_df.to_csv(index=False).encode('utf-8'),
            file_name="prediksi_status_mahasiswa.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data atau melakukan prediksi. Pastikan format CSV Anda benar dan berisi semua kolom yang diperlukan. Error: {e}")
        st.exception(e) 

st.markdown("---")
st.header("Petunjuk Penggunaan:")
st.markdown("""
1.  **Siapkan data Anda:** Pastikan file CSV Anda memiliki semua kolom asli yang sama persis (nama dan tipe data) seperti yang digunakan saat melatih model.
    * Contoh Kolom yang Dibutuhkan (nama asli, bukan yang sudah digrup atau di-encode):
        * `Marital_status`, `Application_mode`, `Course`, `Daytime_evening_attendance`, `Previous_qualification`, `Nacionality`, `Mothers_qualification`, `Fathers_qualification`, `Mothers_occupation`, `Fathers_occupation`, `Displaced`, `Educational_special_needs`, `Debtor`, `Tuition_fees_up_to_date`, `Gender`, `Scholarship_holder`, `International`
        * `Age_at_enrollment`, `Unemployment_rate`, `Inflation_rate`, `GDP`, `Previous_qualification_grade`, `Admission_grade`
        * `Curricular_units_1st_sem_credited`, `Curricular_units_1st_sem_enrolled`, `Curricular_units_1st_sem_evaluations`, `Curricular_units_1st_sem_approved`, `Curricular_units_1st_sem_grade`, `Curricular_units_1st_sem_without_evaluations`
        * `Curricular_units_2nd_sem_credited`, `Curricular_units_2nd_sem_enrolled`, `Curricular_units_2nd_sem_evaluations`, `Curricular_units_2nd_sem_approved`, `Curricular_units_2nd_sem_grade`, `Curricular_units_2nd_sem_without_evaluations`
2.  **Unggah File CSV:** Gunakan tombol "Pilih file CSV" di atas untuk mengunggah file Anda.
3.  **Lihat Hasil:** Aplikasi akan memproses data dan menampilkan hasil prediksi langsung. Anda juga bisa mengunduh hasilnya dalam format CSV.
""")