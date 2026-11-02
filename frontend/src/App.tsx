import {useEffect, useState, type ReactNode} from 'react';
import {NavLink, Route, Routes, useLocation} from 'react-router-dom';
import {Activity, ArrowUpRight, BarChart3, Camera, ChevronRight, CircleDot, ClipboardList, Cpu, FileSearch, Gauge, Layers3, Menu, Settings2, ShieldAlert, X} from 'lucide-react';
import {api, type Health} from './api';
import OverviewPage from './pages/Overview';
import InspectPage from './pages/Inspect';
import HistoryPage from './pages/History';
import SettingsPage from './pages/Settings';
import ResearchPage from './pages/Research';

const links = [
  {path:'/',label:'Command center',icon:BarChart3},
  {path:'/inspect',label:'Visual inspection',icon:Camera},
  {path:'/history',label:'Analysis archive',icon:ClipboardList},
  {path:'/research',label:'Model & evidence',icon:FileSearch},
  {path:'/settings',label:'Monitor settings',icon:Settings2},
];
export default function App(){
 const [health,setHealth]=useState<Health|null>(null);
 const [menu,setMenu]=useState(false);
 const location=useLocation();
 useEffect(()=>{let active=true;const refresh=()=>api.get<Health>('/health').then(r=>{if(active)setHealth(r.data)}).catch(()=>{if(active)setHealth(null)});refresh();const id=setInterval(refresh,20000);return()=>{active=false;clearInterval(id)}},[]);
 useEffect(()=>{setMenu(false)},[location.pathname]);
 const current=links.find(l=>l.path===location.pathname)||links[0];
 return <div className="app-shell">
 <aside className={'sidebar '+(menu?'visible':'')}>
 <div className="brand"><span className="brand-mark"><Layers3 size={22}/></span><div><strong>CONVEYOR<span>JAM</span></strong><small>WATCH / INTELLIGENCE</small></div></div>
 <div className="sidebar-section">WORKSPACE <span>01</span></div>
 <nav className="nav">{links.map(({path,label,icon:Icon})=><NavLink key={path} to={path} end={path==='/'} className={({isActive})=>`nav-item ${isActive?'active':''}`}><Icon size={18}/><span>{label}</span>{path==='/inspect'&&<span className="nav-tag">LIVE</span>}</NavLink>)}</nav>
 <div className="side-bottom"><div className="device-card"><div className="device-orb"><Cpu size={21}/></div><div><span className="eyebrow">COMPUTE ENGINE</span><strong>{health?.device==='cpu'?'CPU / LOCAL':health?.device?'GPU / '+health.device:'NOT CONNECTED'}</strong></div></div><div className="sidebar-note"><ShieldAlert size={16}/><span>Research prototype. Alerts require operator confirmation.</span></div><div className="side-version">CVJW — 01.00.00 <span>DAY 29 / 100</span></div></div>
 </aside>
 {menu&&<div className="mobile-shade" onClick={()=>setMenu(false)}/>}
 <main className="main"><header className="topbar"><div className="left-top"><button className="mobile-menu" onClick={()=>setMenu(!menu)} aria-label="Toggle navigation"><Menu size={21}/></button><span className="breadcrumb">PLATFORM</span><ChevronRight size={14}/><span className="breadcrumb-current">{current.label}</span></div><div className="top-actions"><span className="top-clock"><CircleDot size={14}/> OPERATIONS DESK</span><span className={'connection '+(health?.model_ready?'ready':health?'warning':'offline')}><span className="pulse"/>{health?.model_ready?'MODEL READY':health?'MODEL MISSING':'API OFFLINE'}</span><div className="avatar">CW</div></div></header>
 <div className="page-container"><Routes><Route path="/" element={<OverviewPage health={health}/>}/><Route path="/inspect" element={<InspectPage modelReady={Boolean(health?.model_ready)}/>}/><Route path="/history" element={<HistoryPage/>}/><Route path="/research" element={<ResearchPage/>}/><Route path="/settings" element={<SettingsPage/>}/></Routes></div>
 <footer className="footer"><span><Activity size={14}/> SENSOR TO SIGNAL. SIGNAL TO DECISION.</span><span>Built for observability, not autonomous control <ArrowUpRight size={14}/></span></footer>
 </main></div>
}
export function PageHead({kicker,title,description,action}:{kicker:string;title:string;description:string;action?:ReactNode}){return <div className="page-head"><div><span className="section-kicker"><span className="tiny-line"/>{kicker}</span><h1>{title}</h1><p>{description}</p></div>{action}</div>}
export function Panel({title,sub,children,extra}:{title:string;sub?:string;children:ReactNode;extra?:ReactNode}){return <section className="panel"><div className="panel-head"><div><h3>{title}</h3>{sub&&<p>{sub}</p>}</div>{extra}</div>{children}</section>}
export function Empty({title='Nothing here yet',body='Results appear after your first analysis.'}:{title?:string;body?:string}){return <div className="empty"><Gauge size={30}/><h4>{title}</h4><p>{body}</p></div>}
export function Metric({icon:Icon,label,value,detail,tone='normal'}:{icon:typeof Activity;label:string;value:string|number;detail:string;tone?:string}){return <div className={'metric '+tone}><div className="metric-top"><span>{label}</span><Icon size={20}/></div><strong>{value}</strong><div className="metric-detail"><ArrowUpRight size={14}/>{detail}</div></div>}
