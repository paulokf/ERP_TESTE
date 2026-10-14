import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { medicalReportService, CreateReportPayload } from '@/services/medicalReportService';

export function useMedicalReports(patientId: string) {
  const queryClient = useQueryClient();

  const reportsQuery = useQuery({
    queryKey: ['medical-reports', patientId],
    queryFn: () => medicalReportService.listReports(patientId),
    enabled: !!patientId,
  });

  const createReportMutation = useMutation({
    mutationFn: (payload: CreateReportPayload) =>
      medicalReportService.createReport(patientId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['medical-reports', patientId] });
    },
  });

  return {
    reports: reportsQuery.data || [],
    isLoading: reportsQuery.isLoading,
    isError: reportsQuery.isError,
    error: reportsQuery.error,
    createReport: createReportMutation.mutateAsync,
    isSubmitting: createReportMutation.isPending,
  };
}
