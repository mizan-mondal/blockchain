import zipfile
import xml.etree.ElementTree as ET
import copy
import os

# XML namespaces used in WordprocessingML
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml'
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

W_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP_NAMESPACE = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"

def w_tag(tag):
    return f"{W_NAMESPACE}{tag}"

def wp_tag(tag):
    return f"{WP_NAMESPACE}{tag}"

WEEKS_DATA = [
    {
        "week_num": 1,
        "date_range": "31 – 08 – 2026 to 04 – 09 – 2026",
        "targets": [
            "Conduct literature survey on decentralized edge transaction architectures (LNMesh, Bitchat, hardware-bound CBDCs).",
            "Formulate the Edge Transaction Trilemma (Cloud Latency vs Blockchain Overhead vs Replay Vulnerabilities).",
            "Establish core quantifiable design targets (sub-50ms local commitment, 60s dynamic hash validity, cloud independence).",
            "Define high-level two-phase decoupled execution workflow."
        ],
        "achievements": [
            "Completed comparative study of existing offline payment systems, identifying bottlenecks of pre-funded channels and store-and-forward relays.",
            "Formulated formal problem statement and architectural mission for resource-constrained edge transaction networks.",
            "Specified mathematical foundations for dynamic 60-second rotating HMAC-SHA256 authorization tokens with epoch windows.",
            "Documented two-phase architecture separating zero-latency local P2P commitment from asynchronous mesh consensus."
        ],
        "future_plans": "Implement core cryptographic primitives, user edge wallet structure, keypair management, dynamic rotating hash engine, and initial transaction serialization schema.",
        "days": {
            "Monday": "Held project kickoff meeting with Faculty Guide Mr. Tamoghna Mukherjee; reviewed minor project scope and defined requirements for decentralized transactions in disconnected edge environments.",
            "Tuesday": "Conducted literature survey on existing offline payment architectures (LNMesh, UPI-Offline-Mesh, CBDC hardware solutions) and analyzed their communication overheads and failure modes.",
            "Wednesday": "Formulated the Edge Transaction Trilemma (Cloud Latency vs Blockchain Overhead vs Wireless Replay Attacks) and drafted the refined formal problem statement.",
            "Thursday": "Designed the mathematical specification for the dynamic 60-second rotating hash engine (HMAC-SHA256 with epoch windows) to eliminate wireless packet sniffing and replay attacks.",
            "Friday": "Finalized system architectural blueprint, specifying the two-phase transaction lifecycle decoupling instant local commitment from asynchronous mesh consensus."
        }
    },
    {
        "week_num": 2,
        "date_range": "07 – 09 – 2026 to 11 – 09 – 2026",
        "targets": [
            "Implement secure edge user wallet class with public/private keypair generation and address derivation.",
            "Develop dynamic 60-second rotating hash token generator and verifier engine.",
            "Design standard transaction schema, JSON serialization, and cryptographic signature routines.",
            "Implement temporal epoch window verification with +/- 1 skew slice tolerance."
        ],
        "achievements": [
            "Built edge user wallet module supporting cryptographic keypair generation (Ed25519/ECDSA) and public-key-derived addressing.",
            "Successfully implemented 60-second auto-rotating HMAC-SHA256 authorization token engine bound to sender credentials and transaction parameters.",
            "Created complete transaction payload structure with monotonic sequence counters (nonces).",
            "Validated digital signature signing/verification pipeline; verified strict rejection of expired tokens (>60 seconds) in test suite."
        ],
        "future_plans": "Develop single-node blockchain core, Genesis Block initialization, immutable SHA-256 block linking, and multi-tier account balance state management.",
        "days": {
            "Monday": "Implemented edge user wallet module with asymmetric cryptographic keypair generation and Base58/Hex address derivation.",
            "Tuesday": "Programmed 60-second rotating hash generator binding current epoch window (EpochWindow = floor(Timestamp / 60)), sender key, transaction payload, and nonce.",
            "Wednesday": "Designed transaction data schema including TxID, sender address, recipient address, amount, monotonic nonce, timestamp, signature, and dynamic token.",
            "Thursday": "Implemented cryptographic signing and verification functions for transaction payloads; integrated anti-replay checks using monotonic nonces.",
            "Friday": "Conducted unit test suite for wallet operations; verified that transactions with tokens older than 60 seconds or invalid signatures are strictly rejected."
        }
    },
    {
        "week_num": 3,
        "date_range": "14 – 09 – 2026 to 18 – 09 – 2026",
        "targets": [
            "Construct single-node blockchain core and initialize Genesis Block.",
            "Implement SHA-256 block linking and tamper-detection validation routines.",
            "Build Account State Manager supporting multi-tier balance tracking (Confirmed vs Reserved/Pending balances).",
            "Develop local Pending Transaction Pool (Mempool) and 7-Point Transaction Validation checklist."
        ],
        "achievements": [
            "Successfully initialized Genesis Block (Index 0, all-zero previous hash) and built immutable SHA-256 block chaining logic.",
            "Implemented tamper-detection mechanism that immediately detects hash divergence when historical blocks are altered.",
            "Created Account State Manager with local balance reservation locks (Available = Confirmed - Reserved/Pending).",
            "Deployed strict 7-Point Validation Pipeline screening transactions for signatures, solvency, freshness, nonces, and payload integrity."
        ],
        "future_plans": "Establish multi-node P2P mesh networking environment with HTTP REST endpoints and bidirectional WebSocket communication across simulated edge nodes.",
        "days": {
            "Monday": "Designed Block data structure (Index, PreviousHash, MerkleRoot, Timestamp, BlockProducer) and created Genesis Block initialization logic.",
            "Tuesday": "Implemented SHA-256 cryptographic chain validation and tamper detection logic (verifying hash continuity between successive blocks).",
            "Wednesday": "Developed local Account State Manager with multi-tier balance tracking and balance reservation locks to prevent local overdrafts.",
            "Thursday": "Built local Pending Transaction Pool (Mempool) with configurable batch sealing triggers based on transaction count and time thresholds.",
            "Friday": "Programmed 7-Point Validation Checklist (verifying signatures, sender legitimacy, solvency, time freshness, nonces, mempool conflicts, and schema integrity)."
        }
    },
    {
        "week_num": 4,
        "date_range": "21 – 09 – 2026 to 25 – 09 – 2026",
        "targets": [
            "Configure multi-node simulation environment running 4 autonomous node instances on distinct ports (8001–8004).",
            "Build HTTP REST API endpoints for state inspection, balance queries, and transaction triggering.",
            "Implement bidirectional WebSocket server and client for peer-to-peer mesh gossip dissemination.",
            "Implement and benchmark Phase 1 zero-latency local P2P commitment handshake (<50ms)."
        ],
        "achievements": [
            "Successfully deployed 4 independent node instances communicating over local loopback ports (8001, 8002, 8003, 8004).",
            "Developed comprehensive REST endpoints (/state, /balance, /mempool, /transact, /chain) for node management.",
            "Established full-duplex WebSocket peer links creating a decentralized mesh without a central coordinator.",
            "Implemented Phase 1 direct handshake: local balance lock, P2P transmission, receiver verification, and instant signed provisional receipt in under 45ms."
        ],
        "future_plans": "Implement Phase 2 asynchronous transaction gossip propagation, compact differential database transfer protocol (State Diffs), and rolling ledger pruning.",
        "days": {
            "Monday": "Configured multi-instance architecture deploying Node 1 (8001), Node 2 (8002), Node 3 (8003), and Node 4 (8004) as autonomous edge processes.",
            "Tuesday": "Built HTTP REST endpoints for node state queries, wallet balance inspection, mempool listing, and manual transaction triggering.",
            "Wednesday": "Implemented bidirectional WebSocket networking layer for direct peer-to-peer mesh messaging, peer discovery, and state broadcasting.",
            "Thursday": "Developed Phase 1 zero-latency local commitment protocol: sender balance reservation, point-to-point payload delivery, and provisional crediting.",
            "Friday": "Benchmarked Phase 1 local commitment latency across simulated edge peers; verified transaction confirmation and receipt issuance in under 45ms."
        }
    },
    {
        "week_num": 5,
        "date_range": "28 – 09 – 2026 to 02 – 10 – 2026",
        "targets": [
            "Implement Phase 2 asynchronous gossip dissemination to all neighboring peer mempools.",
            "Design compact differential database transfer protocol (DeltaPacket structure).",
            "Implement Merkle tree root calculation for account balance state tries.",
            "Develop rolling ledger pruning mechanism to minimize flash storage consumption on edge devices."
        ],
        "achievements": [
            "Implemented asynchronous gossip propagation routing unconfirmed transactions across the 4-node mesh topology.",
            "Developed compact State Diff delta packet protocol propagating net balance and nonce changes rather than full historical blocks.",
            "Integrated Merkle State Root calculation ensuring cryptographic auditability of compact delta transitions.",
            "Deployed rolling block pruning retaining the latest Merkle root and rolling window of N blocks to bound storage overhead to O(delta).",
        ],
        "future_plans": "Simulate network partitioning scenarios, implement partition reconciliation with deterministic reversion, build cold-node fast catch-up, and conduct security testing.",
        "days": {
            "Monday": "Implemented Phase 2 asynchronous gossip dissemination broadcast from transacting nodes to all neighboring peer mempools.",
            "Tuesday": "Designed DeltaPacket schema (BatchID, BaseStateRoot, NewStateRoot, balance/nonce deltas, and block signatures) for lightweight synchronization.",
            "Wednesday": "Programmed Merkle Tree calculation for account state tries; implemented verification of delta transitions on peer nodes.",
            "Thursday": "Implemented batch block sealing and state diff broadcast, transitioning transactions from Pending to Finalized Ledger state.",
            "Friday": "Built rolling ledger pruning mechanism to remove old historical blocks while preserving cryptographic root auditability, saving >85% storage."
        }
    },
    {
        "week_num": 6,
        "date_range": "05 – 10 – 2026 to 09 – 10 – 2026",
        "targets": [
            "Simulate network partitioning by splitting nodes into isolated clusters (Mesh 1: Nodes 1–2, Mesh 2: Nodes 3–4).",
            "Implement deterministic conflict resolution for double-spend mitigation during partition merge.",
            "Build Fast Catch-Up protocol for cold or rejoining nodes using verified state snapshots.",
            "Execute security attack simulations (replay attacks, block modification) and synthesize final performance benchmarks."
        ],
        "achievements": [
            "Demonstrated successful autonomous transaction processing in partitioned offline mesh clusters without cloud connectivity.",
            "Verified deterministic tie-breaking logic during partition merge: duplicate nonces detected and invalid branch reverted.",
            "Successfully tested Fast Catch-Up protocol enabling rejoining nodes to sync state via Merkle snapshots in seconds.",
            "Validated 100% rejection rate against wireless replay attacks and demonstrated instantaneous detection of tampered historical blocks.",
            "Reviewed completed minor project progress and documentation with Faculty Guide Mr. Tamoghna Mukherjee."
        ],
        "future_plans": "Prepare for minor project viva and demonstration; port Python engine to physical hardware (Raspberry Pi / ESP32 edge devices) over Bluetooth Low Energy / Wi-Fi mesh.",
        "days": {
            "Monday": "Simulated physical network partition by isolating Nodes 1 & 2 from Nodes 3 & 4; validated continuous Phase 1 transactions within disconnected sub-nets.",
            "Tuesday": "Engineered deterministic reconciliation logic for partition merge: prioritizing earlier verified timestamps and revoking double-spends.",
            "Wednesday": "Implemented Fast Catch-Up onboarding workflow enabling offline or rejoining nodes to synchronize via state snapshots without full chain replay.",
            "Thursday": "Executed security test suite: validated rejection of captured 60s hash tokens and proved tamper detection upon block mutation.",
            "Friday": "Synthesized quantitative benchmark metrics (<50ms latency, >85% storage reduction); compiled WPR documentation and held guide review."
        }
    }
]

def create_run(text, bold=False, italic=False, font="Times New Roman", size="20", has_tab=False, has_br=False):
    r = ET.Element(w_tag('r'))
    rPr = ET.SubElement(r, w_tag('rPr'))
    if font:
        rFonts = ET.SubElement(rPr, w_tag('rFonts'))
        rFonts.set(w_tag('ascii'), font)
        rFonts.set(w_tag('hAnsi'), font)
    if bold:
        ET.SubElement(rPr, w_tag('b'))
    if italic:
        ET.SubElement(rPr, w_tag('i'))
    if size:
        sz = ET.SubElement(rPr, w_tag('sz'))
        sz.set(w_tag('val'), size)
    if has_tab:
        ET.SubElement(r, w_tag('tab'))
    if has_br:
        ET.SubElement(r, w_tag('br'))
    if text:
        t = ET.SubElement(r, w_tag('t'))
        if text.startswith(' ') or text.endswith(' '):
            t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
    return r

def build_week_elements(template_elements, week_data):
    # Deepcopy all template elements (0 to 35)
    week_elems = [copy.deepcopy(elem) for elem in template_elements]
    week_idx = week_data["week_num"]

    # 1. Update logo drawing id in P0 so it is unique per week
    docPr = week_elems[0].find('.//' + wp_tag('docPr'))
    if docPr is not None:
        docPr.set('id', str(week_idx))
        docPr.set('name', f"Image {week_idx}")

    # 2. Update Week Commencing in P5
    # Original text: For the Week Commencing xx – xx – xxxx to xx – xx – xxxx
    # Replace runs with new date text
    p5 = week_elems[5]
    pPr5 = p5.find(w_tag('pPr'))
    p5.clear()
    if pPr5 is not None:
        p5.append(pPr5)
    p5.append(create_run("For the Week Commencing ", font="Times New Roman", size="20"))
    p5.append(create_run(week_data["date_range"], bold=True, font="Times New Roman", size="20"))

    # 3. P10: Company Name: amity
    p10 = week_elems[10]
    pPr10 = p10.find(w_tag('pPr'))
    tabs10 = pPr10.find(w_tag('tabs')) if pPr10 is not None else None
    if tabs10 is not None:
        has_3780 = any(t.attrib.get(w_tag('pos')) == '3780' for t in tabs10)
        if not has_3780:
            new_tab = ET.SubElement(tabs10, w_tag('tab'))
            new_tab.set(w_tag('val'), 'left')
            new_tab.set(w_tag('pos'), '3780')
    p10.append(create_run("", has_tab=True))
    p10.append(create_run("amity", font="Times New Roman", size="20"))

    # 4. P13: Faculty Guide’s Name: Mr. Tamoghna Mukherjee
    p13 = week_elems[13]
    p13.append(create_run("Mr. Tamoghna Mukherjee", font="Times New Roman", size="20"))

    # 5. P19: Project Title: Decentralized Blockchain based  Transaction System on Edge deveces
    p19 = week_elems[19]
    p19.append(create_run("Decentralized Blockchain based  Transaction System on Edge deveces", font="Times New Roman", size="20"))

    # 6. P22: Targets for the week:
    p22 = week_elems[22]
    pPr22 = p22.find(w_tag('pPr'))
    if pPr22 is not None:
        ind22 = pPr22.find(w_tag('ind'))
        if ind22 is not None and w_tag('right') in ind22.attrib:
            ind22.attrib[w_tag('right')] = '180'
    p22.clear()
    if pPr22 is not None:
        p22.append(pPr22)
    p22.append(create_run("Targets for the week:", bold=True, font="Times New Roman", size="20"))
    for i, target in enumerate(week_data["targets"]):
        p22.append(create_run("", has_br=True))
        p22.append(create_run(f"  •  {target}", font="Times New Roman", size="19"))

    # 7. P23: Achievements for the week:
    p23 = week_elems[23]
    pPr23 = p23.find(w_tag('pPr'))
    if pPr23 is not None:
        ind23 = pPr23.find(w_tag('ind'))
        if ind23 is not None and w_tag('right') in ind23.attrib:
            ind23.attrib[w_tag('right')] = '180'
    p23.clear()
    if pPr23 is not None:
        p23.append(pPr23)
    p23.append(create_run("Achievements for the week:", bold=True, font="Times New Roman", size="20"))
    for i, ach in enumerate(week_data["achievements"]):
        p23.append(create_run("", has_br=True))
        p23.append(create_run(f"  •  {ach}", font="Times New Roman", size="19"))

    # 8. P24: Future work plans:
    p24 = week_elems[24]
    pPr24 = p24.find(w_tag('pPr'))
    if pPr24 is not None:
        ind24 = pPr24.find(w_tag('ind'))
        if ind24 is not None and w_tag('right') in ind24.attrib:
            ind24.attrib[w_tag('right')] = '180'
    p24.clear()
    if pPr24 is not None:
        p24.append(pPr24)
    p24.append(create_run("Future work plans: ", bold=True, font="Times New Roman", size="20"))
    p24.append(create_run(week_data["future_plans"], font="Times New Roman", size="19"))

    # 9. P28: Table (Days / Time, Monday to Friday)
    tbl = week_elems[28]
    rows = tbl.findall(w_tag('tr'))
    
    # Row 0: Headers
    tc0_0 = rows[0].findall(w_tag('tc'))[0]
    tc0_0.clear()
    tcPr0_0 = ET.SubElement(tc0_0, w_tag('tcPr'))
    tcW0_0 = ET.SubElement(tcPr0_0, w_tag('tcW'))
    tcW0_0.set(w_tag('w'), '1963')
    tcW0_0.set(w_tag('type'), 'dxa')
    p_head0 = ET.SubElement(tc0_0, w_tag('p'))
    pPr_head0 = ET.SubElement(p_head0, w_tag('pPr'))
    pStyle0 = ET.SubElement(pPr_head0, w_tag('pStyle'))
    pStyle0.set(w_tag('val'), 'TableParagraph')
    sp0 = ET.SubElement(pPr_head0, w_tag('spacing'))
    sp0.set(w_tag('before'), '60')
    sp0.set(w_tag('after'), '60')
    jc0 = ET.SubElement(pPr_head0, w_tag('jc'))
    jc0.set(w_tag('val'), 'center')
    p_head0.append(create_run("Days / Time", bold=True, font="Verdana", size="18"))

    tc0_1 = rows[0].findall(w_tag('tc'))[1]
    tc0_1.clear()
    tcPr0_1 = ET.SubElement(tc0_1, w_tag('tcPr'))
    tcW0_1 = ET.SubElement(tcPr0_1, w_tag('tcW'))
    tcW0_1.set(w_tag('w'), '8094')
    tcW0_1.set(w_tag('type'), 'dxa')
    p_head1 = ET.SubElement(tc0_1, w_tag('p'))
    pPr_head1 = ET.SubElement(p_head1, w_tag('pPr'))
    pStyle1 = ET.SubElement(pPr_head1, w_tag('pStyle'))
    pStyle1.set(w_tag('val'), 'TableParagraph')
    sp1 = ET.SubElement(pPr_head1, w_tag('spacing'))
    sp1.set(w_tag('before'), '60')
    sp1.set(w_tag('after'), '60')
    jc1 = ET.SubElement(pPr_head1, w_tag('jc'))
    jc1.set(w_tag('val'), 'center')
    p_head1.append(create_run("Summary of Work Executed", bold=True, font="Verdana", size="18"))

    # Days mapping
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for day_i, day_name in enumerate(day_names, start=1):
        row = rows[day_i]
        # tc 0: Day label
        tc_day = row.findall(w_tag('tc'))[0]
        tc_day.clear()
        tcPr_d = ET.SubElement(tc_day, w_tag('tcPr'))
        tcW_d = ET.SubElement(tcPr_d, w_tag('tcW'))
        tcW_d.set(w_tag('w'), '1963')
        tcW_d.set(w_tag('type'), 'dxa')
        p_d = ET.SubElement(tc_day, w_tag('p'))
        pPr_d = ET.SubElement(p_d, w_tag('pPr'))
        pSt_d = ET.SubElement(pPr_d, w_tag('pStyle'))
        pSt_d.set(w_tag('val'), 'TableParagraph')
        sp_d = ET.SubElement(pPr_d, w_tag('spacing'))
        sp_d.set(w_tag('before'), '60')
        sp_d.set(w_tag('after'), '60')
        jc_d = ET.SubElement(pPr_d, w_tag('jc'))
        jc_d.set(w_tag('val'), 'center')
        p_d.append(create_run(day_name, bold=True, font="Verdana", size="18"))

        # tc 1: Day tasks
        tc_task = row.findall(w_tag('tc'))[1]
        tc_task.clear()
        tcPr_t = ET.SubElement(tc_task, w_tag('tcPr'))
        tcW_t = ET.SubElement(tcPr_t, w_tag('tcW'))
        tcW_t.set(w_tag('w'), '8094')
        tcW_t.set(w_tag('type'), 'dxa')
        p_t = ET.SubElement(tc_task, w_tag('p'))
        pPr_t = ET.SubElement(p_t, w_tag('pPr'))
        pSt_t = ET.SubElement(pPr_t, w_tag('pStyle'))
        pSt_t.set(w_tag('val'), 'TableParagraph')
        sp_t = ET.SubElement(pPr_t, w_tag('spacing'))
        sp_t.set(w_tag('before'), '40')
        sp_t.set(w_tag('after'), '40')
        sp_t.set(w_tag('line'), '240')
        sp_t.set(w_tag('lineRule'), 'auto')
        ind_t = ET.SubElement(pPr_t, w_tag('ind'))
        ind_t.set(w_tag('left'), '120')
        ind_t.set(w_tag('right'), '120')
        p_t.append(create_run(week_data["days"][day_name], font="Times New Roman", size="19"))

    # 10. Adjust spacer paragraphs before signature
    spacer = week_elems[29]
    spacer.clear()
    pPr_sp = ET.SubElement(spacer, w_tag('pPr'))
    pSt_sp = ET.SubElement(pPr_sp, w_tag('pStyle'))
    pSt_sp.set(w_tag('val'), 'BodyText')
    sp_val = ET.SubElement(pPr_sp, w_tag('spacing'))
    sp_val.set(w_tag('before'), '120')

    # Selected elements to return for this week:
    # 0 to 28 (Header up to Table) + spacer + 34 (Signatures) + 35 (Empty line)
    final_week_elems = week_elems[:29] + [spacer, week_elems[34], week_elems[35]]

    # If not the last week, append a page break paragraph
    if week_idx < 6:
        pb_p = ET.Element(w_tag('p'))
        pb_r = ET.SubElement(pb_p, w_tag('r'))
        pb_br = ET.SubElement(pb_r, w_tag('br'))
        pb_br.set(w_tag('type'), 'page')
        final_week_elems.append(pb_p)

    return final_week_elems

def generate_full_wpr():
    template_docx = 'docs/Sample_WPR_Original_Template.docx'
    output_docx = 'docs/Sample_WPR.docx'

    with zipfile.ZipFile(template_docx, 'r') as z_in:
        xml_content = z_in.read('word/document.xml')
        all_files = {name: z_in.read(name) for name in z_in.namelist()}

    tree = ET.fromstring(xml_content)
    body = tree.find(w_tag('body'))
    
    # In the template body, children 0 to 35 are the week template; child 36 is sectPr
    children = list(body)
    template_elems = children[:-1] # 0 to 35
    sectPr = children[-1]          # sectPr

    # Clear body
    body.clear()

    # Build each week
    for week_data in WEEKS_DATA:
        week_elems = build_week_elements(template_elems, week_data)
        for elem in week_elems:
            body.append(elem)

    # Finally append sectPr
    body.append(sectPr)

    # Serialize new document.xml
    new_document_xml = ET.tostring(tree, encoding='utf-8', xml_declaration=True)
    all_files['word/document.xml'] = new_document_xml

    # Write out the updated docx
    with zipfile.ZipFile(output_docx, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for name, data in all_files.items():
            z_out.writestr(name, data)

    print(f"Successfully generated {output_docx} with {len(WEEKS_DATA)} weeks of WPR!")

if __name__ == '__main__':
    generate_full_wpr()
