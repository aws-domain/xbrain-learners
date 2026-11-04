# ICMP và ping: vì sao rule SSH 22 không cho ping được

## 📌 Tổng quan cốt lõi (Core Concepts)
*Security group lọc theo **giao thức + port + nguồn**. Mỗi giao thức cần rule riêng, nên mở TCP 22 không kéo theo việc mở ICMP.*
- **ICMP** là giao thức dùng để kiểm tra và báo lỗi mạng. Công cụ quen thuộc nhất là `ping` (echo request/reply) và `traceroute`.
- **ICMP không có port.** Khác với TCP/UDP, rule ICMP chỉ chọn *loại* (type) và *mã* (code), không có khái niệm "port 22".
- **SSH, HTTP, HTTPS, MySQL chạy trên TCP**, nên không cần ICMP. Chỉ khi dùng `ping` hoặc `traceroute` mới cần mở ICMP.
- **Route đúng chưa chắc thông.** Route `local` chỉ cho biết có đường đi. Gói tin vẫn phải qua SG (lớp instance) và NACL (lớp subnet).
- **Mặc định SG chặn mọi inbound**, kể cả ICMP. Không có rule khớp thì gói tin bị bỏ im lặng, nên `ping` chỉ treo chứ không báo lỗi.

---

## 📐 Sơ đồ Hoạt động (Architectural Flows)

```
 cap-tmp-web ── ping (ICMP echo request) ──► cap-tmp-app-sg
                                              rule hiện có: TCP 22
                                              ICMP không khớp rule nào → DROP

 Thêm rule: Type "All ICMP - IPv4", Source = cap-tmp-web-sg
                                              ICMP khớp rule → PASS
 cap-tmp-web ◄── echo reply (SG stateful, tự cho qua) ── cap-tmp-app
```

Source là `cap-tmp-web-sg` (tham chiếu SG theo SG) nghĩa là chỉ instance thuộc web SG mới ping được vào app. Không cần biết IP cụ thể.

---

## ⚖️ Bảng So Sánh Trực Quan (Comparative Analysis)

### SSH và ping khác nhau ở đâu
| Tiêu chí | SSH | ping |
|---|---|---|
| Giao thức | TCP | ICMP |
| Port | 22 | Không có |
| Rule SG cần | `SSH` (TCP 22) | `All ICMP - IPv4` hoặc `Custom ICMP - Echo Request` |
| Mục đích | Đăng nhập vào máy | Hỏi "máy bên kia còn sống không?" |

### ICMP trong SG và NACL
| Tiêu chí | Security Group | NACL |
|---|---|---|
| Trạng thái | Stateful | Stateless |
| Cần mở chiều trả lời | Không, echo reply tự được phép | **Có**, phải cho cả echo request lẫn echo reply |
| Ephemeral ports 1024-65535 | Không liên quan | **Không áp dụng cho ICMP** vì ICMP không có port |
| Có thể Deny | Không | Có |

### Chẩn đoán nhanh theo triệu chứng
| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| Ping fail, TCP (SSH/HTTP) thông | SG đích hoặc NACL thiếu ICMP |
| Ping thông, SSH fail | SG chưa mở TCP 22, hoặc SSH chưa xác thực được (thiếu key pair) |
| Cả hai fail | Route, SG hoặc NACL chặn cả hai, hoặc instance sai subnet |

---

## 🛠️ Cách kiểm tra kết nối mà không cần ICMP

Muốn biết port TCP có tới được không, thử trực tiếp port đó thay vì ping:

```bash
# Cách 1: nếu máy có nc
nc -zv <private-ip-app> 22

# Cách 2: không cần cài thêm gì
timeout 3 bash -c '</dev/tcp/<private-ip-app>/22' && echo open || echo closed
```

- `open`/`succeeded`: route, SG và NACL đều ổn, nếu SSH vẫn fail thì lỗi nằm ở xác thực.
- Treo rồi timeout: SG hoặc NACL đang chặn, hoặc sai route.
- `Connection refused`: gói tin tới được instance nhưng không có dịch vụ nào listen ở port đó.

SSH từ web sang app qua mạng thì được, nhưng cần **key pair** của app. Nếu app launch không có key pair, SSH báo `Permission denied (publickey)` dù mạng đã thông. Muốn vào shell app thì dùng **SSM Session Manager** trực tiếp, không cần mở port 22.

## ⚠️ Những điểm hay ra đề / dễ nhầm
- **"Ping fail nhưng TCP thông"** → kiểm tra SG/NACL có cho ICMP chưa. Nhiều server cố ý chặn ICMP nên ping fail không có nghĩa mạng hỏng.
- **Timeout** (không phải refused) là dấu hiệu SG/NACL chặn. **Refused** là tới được máy nhưng không có dịch vụ.
- **SG stateful** thì chỉ cần mở chiều vào. **NACL stateless** thì cho ICMP phải mở cả hai chiều (echo request type 8 và echo reply type 0).
- **Đừng chặn toàn bộ ICMP** nếu không cần. ICMP "Fragmentation Needed" (type 3, code 4) phục vụ Path MTU Discovery, chặn nó có thể làm một số kết nối TCP chạy chậm hoặc treo với gói tin lớn.
- **Tham chiếu SG theo SG** (`Source = sg-...`) thay vì theo IP giúp rule vẫn đúng khi instance đổi IP.

## 🔗 Liên quan
- Stateful (SG) vs Stateless (NACL), ephemeral ports: [stateful_vs_stateless_connections.md](./stateful_vs_stateless_connections.md)
- Route và public IP quyết định ra Internet: [public_ip_vs_route_igw_nat_flow.md](./public_ip_vs_route_igw_nat_flow.md)
- Nguồn thực hành: capstone `cap1-1` (Mạng VPC) trong `aws-certification/soa-co3/capstones/cap1-web-platform/ch1-vpc-network`
