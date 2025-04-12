export interface Campaign {
  name: string;
  variant: string;
  subjectLine: string;
  content: string;
  recipients: number;
  clicks?: number;
  purchases?: number;
}
