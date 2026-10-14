import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface MedicalReport {
  id: string;
  patient_id: string;
  doctor_id: string;
  doctor_name: string;
  doctor_crm?: string;
  appointment_id?: string;
  tuss_code: string;
  procedure_name: string;
  cid10_code: string;
  cid10_description: string;
  eye_laterality: 'OD' | 'OE' | 'OU';
  clinical_indication?: string;
  report_body: string;
  diagnostic_conclusion: string;
  file_name: string;
  file_content_type: string;
  file_size_bytes: number;
  sha256_hash: string;
  signed_at: string;
  created_at: string;
}

export interface CreateReportPayload {
  tuss_code: string;
  procedure_name: string;
  cid10_code: string;
  cid10_description: string;
  eye_laterality: string;
  clinical_indication?: string;
  report_body: string;
  diagnostic_conclusion: string;
  appointment_id?: string;
  file: File;
}

export const medicalReportService = {
  async listReports(patientId: string): Promise<MedicalReport[]> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    const response = await axios.get(`${API_URL}/patients/${patientId}/reports`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    return response.data;
  },

  async createReport(patientId: string, payload: CreateReportPayload): Promise<MedicalReport> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    const { file, ...meta } = payload;

    const formData = new FormData();
    formData.append('metadata_json', JSON.stringify(meta));
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/patients/${patientId}/reports`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });
    return response.data;
  },

  getReportImageUrl(patientId: string, reportId: string): string {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : '';
    return `${API_URL}/patients/${patientId}/reports/${reportId}/image?token=${token}`;
  },
};
