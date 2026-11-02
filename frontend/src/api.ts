import axios from 'axios';
export const api = axios.create({baseURL: '/api/v1',timeout: 180000});
export type Health = {status:string; model_ready:boolean;model_loaded:boolean;model_path:string;device:string;mode:string;timestamp:string};
export type Event = {track_id:number; time_seconds:number; class:string; reason:string;verified_jam:boolean};
export type Detection = {class_id:number;label:string;confidence:number;bbox:number[];track_id:number|null};
export type RecordItem = {id:string;created_at:string;kind:string;status:string;filename:string;detections:number;alerts:number;processing_seconds:number;artifact:string|null;artifact_url?:string;details:{objects?:Detection[];events?:Event[];processed_frames?:number;duration_seconds?:number;processing_fps?:number;tracking_observations?:number;[key:string]:unknown}};
export type Overview = {stats:{analyses:number;alerts:number;detections:number};activity:{day:string;analyses:number;alerts:number}[];model_ready:boolean;notice:string};
export type Config = {dwell_seconds:number;stationary_px_per_second:number;roi:[number,number,number,number];min_observations:number;lost_reset_seconds:number};
export function artifactUrl(url?:string|null){return url || undefined;}
export function errMessage(e:unknown){if(axios.isAxiosError(e)){const data=e.response?.data;return typeof data?.detail==='string'?data.detail:e.message;}return e instanceof Error?e.message:'Unexpected error';}
