import { v4 as uuid } from 'uuid';

export interface LoopData {
  id: string;
  createdTime: string;
  fields: LoopDataFields;
}

export interface LoopDataFields {
  ["Created Time"]?: string;
  Download: string;
  Number?: number;
  bit_depth: number;
  channels: number;
  creator?: string;
  duration: number;
  link?: string;
  sample_rate: number;
  samples: number;
  session?: string;
}