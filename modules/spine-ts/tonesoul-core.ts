// ToneSoul (魂語) Core - TypeScript Interface
// AI Ethics - Soul Integrity Vow & Responsibility Chain Collaborative Framework

export type SoulIntegrity = 'verified' | 'pending' | 'failed';

export interface SoulVow {
  vowId: string;
  content: string;
  source: string;
  timestamp: string;
  integrityHash: string;
  status: SoulIntegrity;
}

export interface SoulCheckpoint {
  checkpointId: string;
  vowId: string;
  verificationTime: string;
  result: boolean;
  checker: string;
  notes?: string;
}

export interface ToneSoulEvent {
  eventType: 'vow_created' | 'vow_verified' | 'chain_updated' | 'vow_failed';
  data: any;
}

export interface ToneSoulModule {
  createVow(content: string, source: string): SoulVow;
  verifyVow(vowId: string, checker: string): boolean;
  addToResponsibilityChain(actor: string): void;
  getVow(vowId: string): SoulVow | undefined;
  getVowHistory(vowId: string): {
    vow: SoulVow;
    checkpoints: SoulCheckpoint[];
    responsibilityChain: string[];
  } | undefined;
  registerListener(callback: (event: ToneSoulEvent) => void): void;
}

// Example class implementation (for engineering reference)
export class ToneSoulCore implements ToneSoulModule {
  public vows: Map<string, SoulVow> = new Map();
  public checkpoints: Map<string, SoulCheckpoint> = new Map();
  public responsibilityChain: string[] = [];
  private listeners: ((event: ToneSoulEvent) => void)[] = [];

  createVow(content: string, source: string): SoulVow {
    const vowId = this._generateId();
    const integrityHash = this._computeIntegrity(content + source);
    const vow: SoulVow = {
      vowId,
      content,
      source,
      timestamp: new Date().toISOString(),
      integrityHash,
      status: 'pending',
    };
    this.vows.set(vowId, vow);
    this._notifyListeners({ eventType: 'vow_created', data: vow });
    return vow;
  }

  verifyVow(vowId: string, checker: string): boolean {
    const vow = this.vows.get(vowId);
    if (!vow) return false;
    const recomputedHash = this._computeIntegrity(vow.content + vow.source);
    const result = recomputedHash === vow.integrityHash;
    const checkpoint: SoulCheckpoint = {
      checkpointId: this._generateId(),
      vowId,
      verificationTime: new Date().toISOString(),
      result,
      checker,
    };
    this.checkpoints.set(checkpoint.checkpointId, checkpoint);
    vow.status = result ? 'verified' : 'failed';
    this._notifyListeners({ eventType: 'vow_verified', data: { vow, checkpoint } });
    return result;
  }

  addToResponsibilityChain(actor: string): void {
    this.responsibilityChain.push(actor);
    this._notifyListeners({ eventType: 'chain_updated', data: { actor, chain: this.responsibilityChain } });
  }

  getVow(vowId: string): SoulVow | undefined {
    return this.vows.get(vowId);
  }

  getVowHistory(vowId: string) {
    const vow = this.vows.get(vowId);
    if (!vow) return undefined;
    const checkpoints = Array.from(this.checkpoints.values()).filter(
      cp => cp.vowId === vowId
    );
    return {
      vow,
      checkpoints,
      responsibilityChain: this.responsibilityChain,
    };
  }

  registerListener(callback: (event: ToneSoulEvent) => void): void {
    this.listeners.push(callback);
  }

  private _generateId(): string {
    return (
      Math.random().toString(36).slice(2) + Date.now().toString(36)
    ).slice(0, 16);
  }

  private _computeIntegrity(data: string): string {
    // Simple hash demo, replace with SHA256 in prod
    let hash = 0;
    for (let i = 0; i < data.length; i++) {
      hash = (hash << 5) - hash + data.charCodeAt(i);
      hash |= 0;
    }
    return Math.abs(hash).toString(16);
  }

  private _notifyListeners(event: ToneSoulEvent): void {
    this.listeners.forEach(listener => {
      try {
        listener(event);
      } catch (e) {
        console.error('Listener error:', e);
      }
    });
  }
}

// Usage Example
// const module = new ToneSoulCore();
// module.registerListener(event => console.log('[TONE SOUL EVENT]', event));
// const vow = module.createVow('保證倫理一致性', 'ai_backend');
// module.verifyVow(vow.vowId, 'checker1');
// module.addToResponsibilityChain('EthicsBoard');
// const history = module.getVowHistory(vow.vowId);
// console.log(history);
