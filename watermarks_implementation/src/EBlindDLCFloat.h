#ifndef E_BLIND_DLC_FLOAT
#define E_BLIND_DLC_FLOAT

#include "Watermark.h"

class EBlindDLCFloat : public Watermark
{
public:
	EBlindDLCFloat(double alpha = -1, double detectThreshold = -1, std::vector<double> reference = std::vector<double>());
	virtual ~EBlindDLCFloat();
	void setAlpha(double alpha);
	void setDetectThreshold(double detectThreshold);
	void setReference(std::vector<double> reference);

	bool embed(std::shared_ptr<VideoFrame> pframe, bool value);
	DetectResult detect(const std::shared_ptr<VideoFrame> pframe);
	bool getCorrelation(const std::shared_ptr<VideoFrame> pframe, double& correlation);

	static std::shared_ptr<VideoFrame> createReference(const std::shared_ptr<VideoFrame> pframe, int maxValue);

private:
	DetectResult detectInternal(const std::shared_ptr<VideoFrame> pframe, double *pcorrelation);

	double                       m_alpha;
	double                       m_detectThreshold;
	std::vector<double>          m_reference;
};

#endif
