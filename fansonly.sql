--
-- PostgreSQL database dump
--

\restrict m1a1cjPQZrQNo6RB6tx4jB20jnLtpboDa4qAoEvIcwe3DgrbybrIcG0EhwZxT0D

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: fansonly_user
--

CREATE TABLE public.refresh_tokens (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    token_hash character varying(255) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    is_revoked boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.refresh_tokens OWNER TO fansonly_user;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: fansonly_user
--

CREATE SEQUENCE public.refresh_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.refresh_tokens_id_seq OWNER TO fansonly_user;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fansonly_user
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: fansonly_user
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    email character varying(255),
    password_hash character varying(255),
    display_name character varying(100) NOT NULL,
    role character varying(20) NOT NULL,
    is_guest boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_email_verified boolean DEFAULT false NOT NULL,
    last_login_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO fansonly_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: fansonly_user
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO fansonly_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: fansonly_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: fansonly_user
--

COPY public.refresh_tokens (id, user_id, token_hash, expires_at, is_revoked, created_at, updated_at) FROM stdin;
1	1	66f2de520b41577be38c179bc804c417c78c40338ee8b35beafce91b4dabc6e9	2026-04-12 21:30:48.790101+05:30	f	2026-03-13 21:30:48.675518+05:30	2026-03-13 21:30:48.675518+05:30
2	1	ed9fa143b09e0f846e744fae8a533c99b1143cfb1ae3178cafaba000402a368d	2026-04-12 21:33:30.310648+05:30	f	2026-03-13 21:33:30.224117+05:30	2026-03-13 21:33:30.224117+05:30
3	2	7a87397d0bd9671807cddc317969a1dbd85c9060ecdd50dce49212bdeb13c0fb	2026-04-13 13:07:41.557918+05:30	f	2026-03-14 13:07:41.471552+05:30	2026-03-14 13:07:41.471552+05:30
4	2	267be322ac7ffb4ef013dc2a93ef4e06a34e5bf28660ef02c9672c8fba06f051	2026-04-13 13:08:08.937323+05:30	f	2026-03-14 13:08:08.88255+05:30	2026-03-14 13:08:08.88255+05:30
5	3	d99fa44ab0cb5ec417f7f0ccf031f3c949b35371be8be4e1461834c9c02d8d2d	2026-04-13 21:05:32.841868+05:30	t	2026-03-14 21:05:32.815304+05:30	2026-03-14 21:06:19.63525+05:30
6	3	659562afe4a0241e611730e3ed9ff9a26e9afc45deae453bd2c1df4056a43acc	2026-04-13 21:06:19.646596+05:30	t	2026-03-14 21:06:19.63525+05:30	2026-03-14 21:07:02.660204+05:30
7	1	706eb607f36851f7332f7570a8ace0749cf90674379b41fce8aff0ee49d843c7	2026-04-13 21:16:40.838144+05:30	f	2026-03-14 21:16:40.757056+05:30	2026-03-14 21:16:40.757056+05:30
8	4	c1f1b3aa76e95155476e10dbc84d61b006a866b05abca74e3d622b17c7696532	2026-04-14 21:49:17.721335+05:30	f	2026-03-15 21:49:17.621303+05:30	2026-03-15 21:49:17.621303+05:30
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: fansonly_user
--

COPY public.users (id, email, password_hash, display_name, role, is_guest, is_active, is_email_verified, last_login_at, created_at, updated_at) FROM stdin;
2	testuser1@example.com	$argon2id$v=19$m=65536,t=3,p=4$v8kLTUxY6TOl04iUwfL+YQ$+mYkuF8EyAiuntddupXiQo6WyDtCBGouNFCv/ZzSECE	Test User	visitor	f	t	f	2026-03-14 13:08:08.936754+05:30	2026-03-14 13:07:41.471552+05:30	2026-03-14 13:08:08.88255+05:30
3	\N	\N	Nishant	visitor	t	t	f	\N	2026-03-14 21:05:32.815304+05:30	2026-03-14 21:05:32.815304+05:30
1	testuser@example.com	$argon2id$v=19$m=65536,t=3,p=4$q9zypNQr98C56NrcWxp9gQ$WLi7ZvwyDPc/hLgv8y3+DiJYfoxNcZrXXlTyfqK6LWs	Test User	visitor	f	t	f	2026-03-14 21:16:40.82219+05:30	2026-03-13 21:30:48.675518+05:30	2026-03-14 21:16:40.757056+05:30
4	nishantsagar045@gmail.com	$argon2id$v=19$m=65536,t=3,p=4$lZbgMNiRkg/UpDVTMp7Eeg$iV4wdwBQg23TmFwB63DaAhZuZJ0+mxeXGxnFMlBdi2k	Nishant Sagar	visitor	f	t	f	\N	2026-03-15 21:49:17.621303+05:30	2026-03-15 21:49:17.621303+05:30
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fansonly_user
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 8, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: fansonly_user
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_hash_key UNIQUE (token_hash);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: fansonly_user
--

CREATE INDEX ix_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: fansonly_user
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: fansonly_user
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict m1a1cjPQZrQNo6RB6tx4jB20jnLtpboDa4qAoEvIcwe3DgrbybrIcG0EhwZxT0D

