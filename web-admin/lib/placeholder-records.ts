export type RecordSummary = {
  id: string;
  record_no: string;
  status: string;
  customer_name: string;
  updated_at: string;
};

export type RecordDetail = RecordSummary & {
  notes: string;
  attachments: string[];
  tags: string[];
};

export const recordData: Record<string, RecordDetail[]> = {
  shipments: [
    {
      id: "shipment-001",
      record_no: "SHP-2026-0001",
      status: "draft",
      customer_name: "北區門市",
      updated_at: "2026-03-08T09:00:00+08:00",
      notes: "等待條碼掃描與附件補齊。",
      attachments: ["front-photo", "packing-slip"],
      tags: ["shipment", "pending-upload"],
    },
    {
      id: "shipment-002",
      record_no: "SHP-2026-0002",
      status: "queued",
      customer_name: "南區經銷商",
      updated_at: "2026-03-08T10:30:00+08:00",
      notes: "已完成基本資料，待上傳 NAS。",
      attachments: ["box-photo"],
      tags: ["shipment"],
    },
  ],
  repairs: [
    {
      id: "repair-001",
      record_no: "RPR-2026-0001",
      status: "received",
      customer_name: "王小明",
      updated_at: "2026-03-08T11:00:00+08:00",
      notes: "待補故障描述附件。",
      attachments: ["device-photo", "service-form"],
      tags: ["repair", "intake"],
    },
  ],
  returns: [
    {
      id: "return-001",
      record_no: "RTN-2026-0001",
      status: "inspection",
      customer_name: "線上商城",
      updated_at: "2026-03-08T12:00:00+08:00",
      notes: "商品外箱有破損，待確認退貨原因。",
      attachments: ["damage-photo"],
      tags: ["return", "inspection"],
    },
  ],
};

export function filterRecords(items: RecordDetail[], q?: string, status?: string) {
  return items.filter((item) => {
    if (status && item.status !== status) {
      return false;
    }

    if (q) {
      const keyword = q.toLowerCase();
      const haystacks = [item.record_no, item.customer_name, item.notes, ...item.tags];
      if (!haystacks.some((value) => value.toLowerCase().includes(keyword))) {
        return false;
      }
    }

    return true;
  });
}