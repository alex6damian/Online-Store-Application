--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

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
-- Name: storeapp_dealer; Type: TABLE; Schema: django; Owner: alex6damian
--

CREATE TABLE django.storeapp_dealer (
    dealer_id integer NOT NULL,
    name character varying(255) NOT NULL,
    phone character varying(10) NOT NULL,
    email character varying(254) NOT NULL,
    address character varying(255)
);


ALTER TABLE django.storeapp_dealer OWNER TO alex6damian;

--
-- Name: storeapp_dealer_dealer_id_seq; Type: SEQUENCE; Schema: django; Owner: alex6damian
--

ALTER TABLE django.storeapp_dealer ALTER COLUMN dealer_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME django.storeapp_dealer_dealer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: storeapp_dealer; Type: TABLE DATA; Schema: django; Owner: alex6damian
--

COPY django.storeapp_dealer (dealer_id, name, phone, email, address) FROM stdin;
1	Nike	0756553918	alexflorea177@gmail.com	Bdul Mihail Kogalniceanu 36-46, Bucuresti
\.


--
-- Name: storeapp_dealer_dealer_id_seq; Type: SEQUENCE SET; Schema: django; Owner: alex6damian
--

SELECT pg_catalog.setval('django.storeapp_dealer_dealer_id_seq', 1, true);


--
-- Name: storeapp_dealer storeapp_dealer_pkey; Type: CONSTRAINT; Schema: django; Owner: alex6damian
--

ALTER TABLE ONLY django.storeapp_dealer
    ADD CONSTRAINT storeapp_dealer_pkey PRIMARY KEY (dealer_id);


--
-- PostgreSQL database dump complete
--

