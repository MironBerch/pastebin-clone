export interface Paste {
  uuid: string;
  title: string;
  created_at: string;
  text?: string;
  expiration?: '10_minutes' | '1_hour' | '1_day' | '1_week' | '1_month' | '1_year' | 'never' | 'burn_after_read';
  exposure?: 'public' | 'unlisted';
}

export interface PasteCreate {
  title: string;
  text: string;
  expiration?: '10_minutes' | '1_hour' | '1_day' | '1_week' | '1_month' | '1_year' | 'never' | 'burn_after_read';
  exposure?: 'public' | 'unlisted';
}

export interface PasteListItem {
  uuid: string;
  title: string;
  created_at: string;
}
